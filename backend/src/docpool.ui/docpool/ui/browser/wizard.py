from AccessControl import Unauthorized
from Acquisition import aq_get
from docpool.base.browser.dpdocument import AddForm
from docpool.base.content.archiving import IArchiving
from docpool.base.utils import get_content_area
from docpool.base.utils import getAllowedDocumentTypes
from docpool.base.utils import getDocumentPoolSite
from docpool.elan.utils import getScenariosForCurrentUser
from docpool.ui import _
from docpool.ui.utils import extract_data
from plone import api
from plone.app.dexterity.interfaces import IDXFileFactory
from plone.app.textfield.value import RichTextValue
from plone.memoize.view import memoize
from Products.CMFPlacefulWorkflow.PlacefulWorkflowTool import WorkflowPolicyConfig_id
from Products.Five import BrowserView
from z3c.form.interfaces import NO_VALUE
from zope.interface import Invalid
from zope.schema import ValidationError
from ZPublisher.HTTPRequest import FileUpload

import logging
import time


logger = logging.getLogger(__name__)


class ContextlessWizard(BrowserView):
    """Base-class for contextless multistep wizards with custom templates."""

    total_steps = 2  # needs to be defined in implementation
    portal_type = "some_type"  # needs to be defined in implementation
    session_base_name = f"{portal_type}_wizard"

    def __init__(self, context, request):
        self.context = context
        self.request = request
        if "_wizard_" in self.__name__:
            self.current_step = self.__name__.split("_wizard_")[-1]
        elif self.__name__.startswith("wizard_"):
            # wizards without type prefix...
            self.current_step = self.__name__.split("wizard_")[-1]
        elif "_wizard" in self.__name__:
            # wizards with only one step...
            self.current_step = 1
        self.is_final_step = int(self.current_step) == self.total_steps
        self.errors = {}
        self.form = self.request.form
        self.session = self.request.SESSION
        if "session_name" in self.request.form:
            self.session_name = self.request.form["session_name"]
        else:
            session_key = time.time()
            self.session_name = self.session_base_name + "_" + str(session_key)
        self.data = self.session.get(self.session_name, {})

    def __call__(self):
        raise NotImplementedError

    def extract_data(self):
        """Extract and validate the form data.
        Extra method to simplify customization.
        """
        data, errors = extract_data(self.portal_type, self.request)
        return data, errors

    def transform_data_for_session(self, data):
        """Apply transforms to allow storage in a session."""
        for key, value in data.items():
            if isinstance(value, FileUpload):
                data[key] = transform_fileupload(value)
            elif isinstance(value, list) and any([isinstance(i, FileUpload) for i in value]):
                data[key] = [transform_fileupload(i) for i in value]
        return data

    def run_custom_validation(self):
        """Custom validation."""
        for name in self.form:
            if name.startswith("_") or name.startswith("form.button"):
                continue
            name = name.split("form.widgets.")[-1]
            value = self.data.get(name, NO_VALUE)
            if value is NO_VALUE:
                return
            try:
                self.validate_custom_field(name, value)
            except (Invalid, ValidationError) as e:
                self.errors[name] = e.args[0]

    def validate_custom_field(self, name, value):
        """If a method 'validate_<fieldname>' exists call it.
        This can be used to validate non-schema-fields.
        """
        method_name = f"validate_{name}"
        if getattr(self, method_name, None) is not None:
            exec(f"self.{method_name}(name, value)")

    @property
    def template(self):
        """The template has to be configured in zcml."""
        return self.index

    def nextURL(self, previous=False):
        """Increment the number at the end of the wizard_view
        and redirect to that next (or previous) step.
        """
        base_name = self.__name__.split("_")[:-1]
        base_name = "_".join(base_name)
        if previous:
            next_step = int(self.current_step) - 1
        else:
            next_step = int(self.current_step) + 1
        next_view = f"{base_name}_{next_step}"
        try:
            next_url = "{url}/@@{next}?session_name={session_name}".format(
                url=self.context.absolute_url(),
                next=next_view,
                session_name=self.session_name,
            )
            self.context.restrictedTraverse(next_view)
        except KeyError:
            # The view is not registered
            logger.info(f"View {next_url} does not exists!")
            next_url = self.context.absolute_url()
        except Unauthorized:
            # The view is protected with a different permission
            logger.info(f"View {next_url} is protected!")
            next_url = self.context.absolute_url()
        logger.debug(f'Redirecting to step "{next_view}" ')
        return next_url

    def is_required(self, field):
        fields = getattr(self, self.required_for_next, [])
        if field in fields:
            return "required"
        return ""


class DPDocumentWizard(ContextlessWizard):
    """Wizard for DPDocuments."""

    total_steps = 3
    portal_type = "DPDocument"
    session_base_name = f"{portal_type}_wizard"

    required_for_1 = []
    required_for_2 = ["container_uid", "entrytype"]
    required_for_3 = ["container_uid", "entrytype", "form.widgets.IDublinCore.title"]

    custom_handled_widgets = [
        "docType",
        "IDublinCore.title",
        "IDublinCore.description",
        "text",
        "ILocalBehaviorSupport.local_behaviors",
    ]

    def __call__(self):
        # Required fields for wizard step
        current_step = int(self.current_step)
        required_for = "required_for_{0}"
        self.required_for_step = required_for.format(current_step)
        self.required_for_next = required_for.format(current_step + 1)

        # Go back if a required field is missing
        for required_value in getattr(self, self.required_for_step, []):
            if required_value not in self.data:
                return self.request.response.redirect(self.nextURL(previous=True))

        # Button handlers
        if self.form.get("form.buttons.cancel", None) is not None:
            return self.request.response.redirect(self.context.absolute_url())
        if self.form.get("form.buttons.back", None) is not None:
            return self.request.response.redirect(self.nextURL(previous=True))

        dp_app_state = api.content.get_view("dp_app_state", self.context, self.request)
        self.app = dp_app_state.appsActivatedByCurrentUser()[0]

        # We can only populate fiels and widgets for the add-form once we have the container
        self.add_form = None
        container_uid = self.data.get("container_uid") or self.form.get("container_uid")
        if container_uid:
            container = api.content.get(UID=container_uid)
            self.add_form = AddForm(container, self.request)
            self.add_form.portal_type = self.portal_type
            self.add_form.update()
            self.add_form.updateWidgets()

        # Prepare some data for display on the form
        if container_uid:
            self.container_title = container.title
            if entrytype_id := self.data.get("entrytype", None):
                brains = api.content.find(
                    context=self.context, portal_type="DocType", id=entrytype_id, unrestricted=True
                )
                entrytype = brains[0]._unrestrictedGetObject()
                self.entrytype_title = entrytype.title
                self.entrytype_icon = entrytype.icon_name

        # Render form
        if self.form.get("form.buttons.continue", None) is None:
            return self.template()

        # Validation using schema fields
        data, errors = self.extract_data()

        data = self.transform_data_for_session(data)
        self.data.update(data)
        self.errors.update(errors)
        self.run_custom_validation()

        if self.errors:
            (
                api.portal.show_message(
                    _(
                        "there_was_an_error_processing_the_form",
                        default="There was an error processing the form!",
                    ),
                    self.request,
                    type="error",
                ),
            )
            logger.info(self.errors)
            return self.template()

        # Process wizard step
        if not self.is_final_step:
            self.session[self.session_name] = self.data
            return self.request.response.redirect(self.nextURL())
        new = self.create_item()
        self.session.delete(self.session_name)
        msg = _(
            "Created ${doktype} '${title}'",
            mapping={"doktype": new.docTypeObj().title, "title": new.title},
        )
        api.portal.show_message(msg, self.request)
        return self.request.response.redirect(self.context.absolute_url() + "/@@listing")

    def get_widget(self, name):
        if not self.add_form:
            return
        if widget := self.add_form.widgets.get(name):
            return widget
        for group in self.add_form.groups:
            if widget := group.widgets.get(name):
                return widget

    def create_item(self):
        """Create the content from the data"""
        fields = [i.name for i in self.add_form.widgets.values()]
        item_dict = {}
        for key, value in self.data.items():
            if isinstance(value, RichTextValue):
                # We need to create a fresh RichTextValue because the one in self.data
                # was created in another request and ZODB refuses to store it with:
                #
                # InvalidObjectReference: ('Attempt to store an object from a foreign
                # database connection', <Connection at 11a946f90>,
                # <RawValueHolder: ...and RichText.>).
                value = RichTextValue(value.raw, "text/html", "text/x-html-safe")
            if key in fields and value:
                # only use field name when setting
                key = key.split(".")[-1]
                item_dict[key] = value

        container = api.content.get(UID=self.data["container_uid"])
        entrytype = self.data["entrytype"]
        new = api.content.create(
            container=container,
            type=self.portal_type,
            docType=entrytype,
            local_behaviors=[self.app],
            **item_dict,
        )
        if attachments := self.data.get("attachments"):
            if not isinstance(attachments, list):
                attachments = [attachments]
            for item in attachments:
                filename = item["filename"]
                content_type = item["content_type"]
                factory = IDXFileFactory(new)
                factory(filename, content_type, item["data"])
        if self.data.get("visibility") == "published" and api.content.get_state(new) != "published":
            portal_workflow = api.portal.get_tool("portal_workflow")
            if "publish" in [i["id"] for i in portal_workflow.getTransitionsFor(new)]:
                api.content.transition(new, transition="publish")
        return new

    @memoize
    def containers(self):
        """All containers (uid, title, level) where the user can add entries."""
        brains = api.content.find(
            context=get_content_area(self.context),
            portal_type="GroupFolder",
            sort_on="sortable_title",
            apps_supported=self.app,
        )
        tree = []
        for brain in brains:
            if IArchiving(brain).is_archive:
                continue
            obj = brain.getObject()
            if item := self.check_tree(obj):
                tree.append(item)
        flat = [i for i in self.flatten(tree)]
        return flat

    def flatten(self, items):
        """Flatten a list of nested dicts."""
        for item in items:
            children = item.pop("children", None)
            yield item
            if children:
                for child in self.flatten(children):
                    yield child

    def check_tree(self, obj, level=0):
        """Walk a directory tree and return data about containers where a user can add."""
        query = {
            "portal_type": [
                "PrivateFolder",
                "SimpleFolder",
                "ReviewFolder",
                "CollaborationFolder",
                "InfoFolder",
            ],
            "apps_supported": self.app,
        }
        if self.entries_the_user_can_add(obj):
            data = {"uid": obj.UID(), "title": obj.title, "level": level}
            data["children"] = [self.check_tree(child, level=level + 1) for child in obj.contentValues(query)]
            return data

    def entries_the_user_can_add(self, container):
        """Brains of DocTypes that the current user can add to a given container."""
        if not api.user.has_permission("Add portal content", obj=container):
            return
        allowed = container.allowedDocTypes
        addable = []
        for doctype_brain in getAllowedDocumentTypes(container):
            if self.app not in doctype_brain.apps_supported:
                continue
            if allowed and doctype_brain.id not in allowed:
                continue
            addable.append(doctype_brain)
        return addable

    def doctypes(self):
        """DocTypes that the user is allowed to create in the form given the uid of a container."""
        container_uid = self.data.get("container_uid") or self.form.get("container_uid")
        if not container_uid:
            all_containers = self.containers()
            if len(all_containers) == 1:
                container_uid = all_containers[0]["uid"]
        if not container_uid:
            return []
        container = api.content.get(UID=container_uid)
        return self.entries_the_user_can_add(container)

    def scenarios(self):
        vocabulary = api.portal.get_vocabulary(
            "docpool.elan.vocabularies.Events", context=getDocumentPoolSite(self.context)
        )
        return vocabulary

    def visibility_options(self):
        container = api.content.get(UID=self.data.get("container_uid"))
        workflow = self.get_workflow_for(container)
        # check if there is a transition "publish" originating from the initial state
        initial = workflow.states[workflow.initial_state]
        if "publish" not in initial.transitions:
            return []

        container_title = container.title
        docpool_title = getDocumentPoolSite(container).title
        options = [
            {
                "value": "private",
                "title": _("Internal"),
                "description": _(
                    "For all users of '${app} ${docpool_title}'",
                    mapping={"app": self.app.upper(), "docpool_title": docpool_title},
                ),
            },
            {
                "value": "published",
                "title": _("Published"),
                "description": _(
                    "Only for member of '${container_title}'", mapping={"container_title": container_title}
                ),
            },
        ]
        return options

    def default_scenario(self):
        query = {
            "context": getDocumentPoolSite(self.context),
            "portal_type": "DPEvent",
            "UID": getScenariosForCurrentUser(),
            "Status": "active",
        }
        default_scenarios = api.content.find(**query)
        if default_scenarios:
            return default_scenarios[0].UID

    def get_workflow_for(self, container):
        """Get workflow from container and future portal_type."""
        wf_id = None
        workflow_tool = api.portal.get_tool("portal_workflow")
        # Inspired by PlacefulWorkflowChain: Find placeful workflow starting at target container
        if wfpolicyconfig := aq_get(container, WorkflowPolicyConfig_id, None):
            if chain := wfpolicyconfig.getPlacefulChainFor(self.portal_type, start_here=True):
                wf_id = chain[0]

        # Default workflow for type
        if not wf_id and (chain := workflow_tool.getChainForPortalType(self.portal_type)):
            wf_id = chain[0]

        if wf_id:
            return workflow_tool.getWorkflowById(wf_id)


def transform_fileupload(value):
    """Transform FileUpload into a dict that can safely be stored in a session."""
    if not value:
        return
    if not isinstance(value, FileUpload):
        return value
    return {
        "data": value.read(),
        "filename": value.filename,
        "content_type": value.headers.get("Content-Type", ""),
    }
