from docpool.base.localbehavior.adapter import isSupported
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.schema import SCHEMA_CACHE
from zope.component import getMultiAdapter

import logging


log = logging.getLogger("docpool.localbehavior")


def additionalSchemata(self):
    """Get additional schemata for forms with local behavior support.

    This method is used to patch Plone's default form behavior to include
    only the schema fields that are appropriate for the current context,
    taking into account local behavior restrictions.

    Returns:
        generator: Additional schema interfaces that should be included in the form
    """
    return getAdditionalSchemataWithLocalbehavior(
        context=self.context, request=self.request, portal_type=self.portal_type
    )


def getAdditionalSchemataWithLocalbehavior(context, portal_type, request):
    """Get additional schemata for this context or portal_type with local behavior filtering.

    This function extends Plone's standard schema enumeration to respect local behavior
    restrictions. It only includes schema interfaces (form fields) from behaviors that
    are both:
    1. Permitted in the current DocumentPool context
    2. Activated by the current user

    This ensures that users only see form fields for applications they have access to
    and have chosen to work with, providing a cleaner and more secure interface.

    Additional form field schemata can be defined in behaviors.

    Usually either context or portal_type should be set, not both.
    The idea is that for edit forms or views you pass in a context
    (and we get the portal_type from there) and for add forms you pass
    in a portal_type (and the context is irrelevant then). If both
    are set, the portal_type might get ignored, depending on which
    code path is taken.

    Args:
        context: The content object context
        portal_type (str): The portal type identifier
        request: The current HTTP request

    Yields:
        Interface: Schema interfaces that should be included in forms
    """
    log.debug("getAdditionalSchemata with context %r and portal_type %s", context, portal_type)
    # Usually an add-form.
    if portal_type is None:
        portal_type = context.portal_type

    # DOCPOOL modification! We only want to see behaviors that are allowed
    # here.
    dp_app_state = getMultiAdapter((context, request), name="dp_app_state")
    available_apps = dp_app_state.appsPermittedForObject(context.REQUEST)
    activated_apps = dp_app_state.appsActivatedByCurrentUser()
    effective_apps = list(set(available_apps).intersection(set(activated_apps)))

    for schema_interface in SCHEMA_CACHE.behavior_schema_interfaces(portal_type):
        if isSupported(effective_apps, schema_interface):
            form_schema = IFormFieldProvider(schema_interface, None)
            if form_schema is not None:
                yield form_schema


def patched_additionalSchemata():
    """Create a property-wrapped version of additionalSchemata for monkey patching.

    This function is used to create a proper property decorator around the
    additionalSchemata method so it can be monkey patched onto Plone's
    DefaultAddForm class.

    Returns:
        property: A property-wrapped version of the additionalSchemata method
    """
    return property(additionalSchemata)  # We get a @property decorated method!


# Monkey patch Plone's DefaultAddForm to use our local behavior-aware schema enumeration
DefaultAddForm.additionalSchemata = patched_additionalSchemata()
