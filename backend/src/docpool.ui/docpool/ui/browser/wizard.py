from AccessControl import Unauthorized
from docpool.base import DocpoolMessageFactory as _
from docpool.base.localbehavior.localbehavior import ILocalBehaviorSupport
from docpool.base.utils import get_content_area
from docpool.base.utils import getAllowedDocumentTypes
from docpool.base.utils import getDocumentPoolSite
from docpool.elan.utils import getScenariosForCurrentUser
from docpool.ui.utils import extract_data
from plone import api
from plone.app.dexterity.interfaces import IDXFileFactory
from plone.app.textfield.value import RichTextValue
from plone.dexterity.browser.add import DefaultAddForm
from Products.Five import BrowserView
from z3c.form.interfaces import NO_VALUE
from zope.interface import Invalid
from zope.schema import ValidationError
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
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
        if not previous:
            next_step = int(self.current_step) + 1
        else:
            next_step = int(self.current_step) - 1
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
    required_for_2 = ["container_uid", "docType"]
    required_for_3 = ["container_uid", "docType", "title"]

    def __call__(self):
        # Required fields for wizard step
        current_step = int(self.current_step)
        required_for = "required_for_{0}"
        self.required_for_step = required_for.format(current_step)
        self.required_for_next = required_for.format(current_step + 1)

        for required_value in getattr(self, self.required_for_step, []):
            if required_value not in self.data:
                return self.request.response.redirect(self.nextURL(previous=True))

        # We can only populate fiels and widgets for the add-form once we have the container
        container = self.data.get("container_uid") or self.form.get("container_uid")
        if container:
            container = api.content.get(UID=container)
            self.add_form = DefaultAddForm(container, self.request)
            self.add_form.portal_type = self.portal_type
            self.add_form.update()

        # Button handler
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
        else:
            new = self.create_item()
            self.session.delete(self.session_name)
            return self.request.response.redirect(new.absolute_url())

    def create_item(self):
        """Create the content from the data"""
        fields = [
            "docType",
            "title",
            "text",
            "scenarios",
        ]

        item_dict = {}
        for k, v in self.data.items():
            if isinstance(v, RichTextValue):
                # We need to create a fresh RichTextValue because the one in self.data
                # was created in another request and ZODB refuses to store it with:
                #
                # InvalidObjectReference: ('Attempt to store an object from a foreign
                # database connection', <Connection at 11a946f90>,
                # <RawValueHolder: ...and RichText.>).
                v = RichTextValue(v.raw, "text/html", "text/x-html-safe")
            if k in fields and v:
                item_dict[k] = v

        container = api.content.get(UID=self.data["container_uid"])
        new = api.content.create(
            container=container,
            type=self.portal_type,
            local_behaviors=["elan"],
            **item_dict,
        )
        if self.data.get("attachments"):
            for item in self.data["attachments"]:
                filename = item["filename"]
                content_type = item["content_type"]
                factory = IDXFileFactory(new)
                factory(filename, content_type, item["data"])
        if self.data.get("visibility") == "published" and api.content.get_state(new) != "published":
            portal_workflow = api.portal.get_tool("portal_workflow")
            if "publish" in portal_workflow.getTransitionsFor(new):
                api.content.transition(new, transition="publish")
        return new

    def containers(self):
        """Return uuid vocabulary of GroupFolders where user can add DPDocuments."""
        brains = api.content.find(
            context=get_content_area(self.context),
            portal_type="GroupFolder",
            sort_on="sortable_title",
        )
        terms = []

        app = ""
        user = api.user.get_current()
        if user:
            active_app = user.getProperty("apps")
            if active_app:
                app = active_app[0]

        for brain in brains:
            obj = brain.getObject()
            if not api.user.has_permission("Add portal content", obj=obj):
                continue

            can_add_entries = False
            for doctype_brain in getAllowedDocumentTypes(obj):
                if obj.allowedDocTypes and doctype_brain.id not in obj.allowedDocTypes:
                    continue
                doctype_obj = doctype_brain.getObject()
                if not doctype_obj.globalAllow:
                    continue
                if app not in ILocalBehaviorSupport(doctype_obj).local_behaviors:
                    continue
                can_add_entries = True
                break

            if can_add_entries:
                terms.append(SimpleTerm(value=brain.UID, token=brain.UID, title=brain.Title))
        return SimpleVocabulary(terms)

    def doctypes(self):
        container = self.data.get("container_uid") or self.form.get("container_uid")
        if not container:
            all_containers = self.containers()
            if len(all_containers) == 1:
                container = all_containers._terms[0].value
        if not container:
            return []
        obj = api.content.get(UID=container)
        app = ""
        user = api.user.get_current()
        if user:
            active_app = user.getProperty("apps")
            if active_app:
                app = active_app[0]
        terms = []
        for brain in getAllowedDocumentTypes(obj):
            if obj.allowedDocTypes and brain.id not in obj.allowedDocTypes:
                continue
            doctype_obj = brain.getObject()
            if not doctype_obj.globalAllow:
                continue
            if app not in ILocalBehaviorSupport(doctype_obj).local_behaviors:
                continue

            terms.append(SimpleTerm(value=brain.id, token=brain.id, title=brain.Title))
        return SimpleVocabulary(terms)

    def scenarios(self):
        vocabulary = api.portal.get_vocabulary(
            "docpool.elan.vocabularies.Events", context=getDocumentPoolSite(self.context)
        )
        return vocabulary

    def visibility_options(self):
        container_title = api.content.get(UID=self.data.get("container_uid")).title
        docpool_title = getDocumentPoolSite(self.context).title
        app = ""
        user = api.user.get_current()
        if user:
            active_app = user.getProperty("apps")
            if active_app:
                app = active_app[0]

        options = [
            (
                "private",
                _("Only for member of '${container_title}'", mapping={"container_title": container_title}),
            ),
            (
                "published",
                _(
                    "For all users of '${app} ${docpool_title}'",
                    mapping={"app": app.upper(), "docpool_title": docpool_title},
                ),
            ),
        ]
        terms = [SimpleTerm(value=i[0], token=i[0], title=i[1]) for i in options]
        return SimpleVocabulary(terms)

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


def transform_fileupload(value):
    """Transform FileUpload into a dict that can be pickled in a session."""
    if not value:
        return
    if not isinstance(value, FileUpload):
        return value
    return {
        "data": value.read(),
        "filename": value.filename,
        "content_type": value.headers.get("Content-Type", ""),
    }
