from AccessControl import Unauthorized
from collective.beaker.interfaces import ISession
from docpool.base import DocpoolMessageFactory as _
from docpool.ui.utils import extract_data
from io import BufferedRandom
from io import BytesIO
from plone import api
from plone.app.dexterity.interfaces import IDXFileFactory
from plone.app.textfield.value import RichTextValue
from Products.Five import BrowserView
from z3c.form.interfaces import NO_VALUE
from zope.interface import Invalid
from zope.schema import ValidationError

import logging
import mimetypes
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
        self.session = ISession(self.request)
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

        # handle attachments
        if attachments := data.get("attachments"):
            if not isinstance(attachments, list):
                attachments = [attachments]
            for attachment in attachments:
                if isinstance(attachment.file, BufferedRandom):
                    # Unwrap io.BufferedRandom because it cannot be pickled by beaker
                    attachment.file = BytesIO(attachment.file.read())

        return data, errors

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
    required_for_2 = ["title"]
    required_for_3 = ["title"]

    def __call__(self):
        # Required fields for wizard step
        current_step = int(self.current_step)
        required_for = "required_for_{0}"
        self.required_for_step = required_for.format(current_step)
        self.required_for_next = required_for.format(current_step + 1)

        for required_value in getattr(self, self.required_for_step, []):
            if required_value not in self.data:
                return self.request.response.redirect(self.nextURL(previous=True))

        # Button handler
        if self.form.get("form.buttons.continue", None) is None:
            return self.template()

        # Validation using schema fields
        data, errors = self.extract_data()

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
            return self.template()

        # Process wizard step
        if not self.is_final_step:
            self.session[self.session_name] = self.data
            return self.request.response.redirect(self.nextURL())
        else:
            new = self.create_item()
            self.session.pop(self.session_name)
            return self.request.response.redirect(new.absolute_url())

    def create_item(self):
        """Create the content from the data"""
        fields = [
            "title",
            "text",
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

        portal = api.portal.get()
        container = portal["bund"]["content"]["Groups"]["bund_group1"]
        new = api.content.create(
            container=container,
            type=self.portal_type,
            local_behaviors=["elan"],
            **item_dict,
        )
        if attachments := self.data.get("attachments"):
            for fileupload in attachments:
                filedata = fileupload.file
                if filedata:
                    filename = fileupload.filename
                    content_type = mimetypes.guess_type(filename)[0] or ""
                    factory = IDXFileFactory(new)
                    factory(filename, content_type, filedata.read())
        return new
