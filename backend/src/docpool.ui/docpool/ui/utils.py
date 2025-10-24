from plone import api
from plone.autoform.interfaces import WIDGETS_KEY
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.utils import iterSchemataForType
from plone.dexterity.utils import resolveDottedName
from plone.supermodel.utils import mergedTaggedValueDict
from plone.z3cform.z2 import processInputs
from Products.CMFPlone.utils import safe_unicode
from z3c.form.error import MultipleErrors
from z3c.form.interfaces import IDataConverter
from z3c.form.interfaces import IErrorViewSnippet
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IManagerValidator
from z3c.form.interfaces import NO_VALUE
from z3c.form.interfaces import NOT_CHANGED
from zope import component
from zope.component import getMultiAdapter
from zope.i18nmessageid import MessageFactory
from zope.interface import Invalid
from zope.schema import interfaces

import logging


ZMF = MessageFactory("zope")
log = logging.getLogger(__name__)


def extract_data(portal_type, request=None):
    """
    Utility method to extract and validate data from a contextless form for a
    dexterity type. It returns the data in a format that can be safely set on
    an item.
    """
    if not request:
        portal = api.portal.get()
        request = portal.REQUEST
    cleanup_form_inputs(request)
    fti = component.getUtility(IDexterityFTI, name=portal_type)
    errors = {}
    data = {}
    for widget_name in request.form:
        name = widget_name
        field_and_schema = get_field_and_schema_for_fieldname(name, fti)
        if field_and_schema:
            field, schema = field_and_schema
            # Here we handle schema-hints.
            # When the widget is configured in the schema by a schema hint
            # this will return a ParameterizedWidget which needs to be
            # called to get the "real" widget
            widgets = mergedTaggedValueDict(schema, WIDGETS_KEY)
            widget = widgets.get(name) or widgets.get(name.split(f"{schema.__name__}.")[-1])
            if widget:
                if isinstance(widget, str):
                    widget = resolveDottedName(widget)
                widget = widget(field, request)
            else:
                # In there is no ParameterizedWidget we use the default widget
                # for this field
                widget = getMultiAdapter((field, request), IFieldWidget)
            widget.update()
            try:
                # ugly hack. Why?
                if widget_name != widget.name:
                    widget.name = widget_name
                raw = widget.extract()
            except MultipleErrors as e:
                errors[name] = e
                log.warning(f"Multiple errors while extracting field: {name}")
                continue

            if raw is NOT_CHANGED:
                # empty field that is not required
                continue

            if raw is NO_VALUE and field.required:
                # empty field that is required
                errors[name] = ZMF("Required input is missing.")
                log.warning(f"Required field have missing value: {name}")
                continue
            elif raw is NO_VALUE:
                # empty field that is not required
                continue

            converter = IDataConverter(widget)
            try:
                value = converter.toFieldValue(safe_unicode(raw))
                field.validate(value)
            except interfaces.RequiredMissing as e:
                errors[name] = e.doc()
                log.warning(f"Required field have missing value: {name}")
                continue
            except interfaces.ConstraintNotSatisfied as e:
                errors[name] = e.doc()
                log.warning(f"Constraint not satisfied for field: {name}")
                log.warning(e)
                continue
            except interfaces.WrongType as e:
                errors[name] = e.doc()
                log.warning(f"Wrong type for field: {name}")
                log.warning(e)
                continue
            except interfaces.ValidationError as e:
                errors[name] = e.doc()
                log.warning(f"ValidationError: {name}")
                log.warning(e)
                continue
            except Invalid as e:
                errors[name] = e.args[0]
                log.warning(f"ValidationError: {name}")
                log.warning(e)

            # Get the datamanager and get the original value
            data[name] = value
        else:
            data[name] = request.form[widget_name]

    # Validate the schema e.g. with invariants
    schema_errors = []
    for schema in iterSchemataForType(fti):
        validator = getMultiAdapter((None, request, None, schema, None), IManagerValidator)
        # validate against the already processed data
        schema_errors += validator.validate(data)
    schema_error_snippets = []
    # turn the error-message into a renderable errorsnippet
    for error in schema_errors:
        view = getMultiAdapter((error, request, None, None, None, None), IErrorViewSnippet)
        view.update()
        schema_error_snippets += (view.message,)
    if schema_error_snippets:
        errors["schema"] = schema_error_snippets

    return data, errors


def cleanup_form_inputs(request):
    """Call processInputs to decode strings to unicode, otherwise the
    z3c.form dataconverters complain.
    """
    processInputs(request)


def get_field_and_schema_for_fieldname(field_id, fti):
    """Get field and its schema from a fti."""
    field_id = field_id.split(".")[-1]
    for schema in iterSchemataForType(fti):
        field = schema.get(field_id, None)
        if field is not None:
            return (field, schema)
