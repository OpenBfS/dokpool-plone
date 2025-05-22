from docpool.base.localbehavior.adapter import isSupported
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.schema import SCHEMA_CACHE
from zope.component import getMultiAdapter

import logging


log = logging.getLogger("docpool.localbehavior")


def additionalSchemata(self):
    return getAdditionalSchemataWithLocalbehavior(
        context=self.context, request=self.request, portal_type=self.portal_type
    )


def getAdditionalSchemataWithLocalbehavior(context, portal_type, request):
    """Get additional schemata for this context or this portal_type.

    Additional form field schemata can be defined in behaviors.

    Usually either context or portal_type should be set, not both.
    The idea is that for edit forms or views you pass in a context
    (and we get the portal_type from there) and for add forms you pass
    in a portal_type (and the context is irrelevant then).  If both
    are set, the portal_type might get ignored, depending on which
    code path is taken.
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
    return property(additionalSchemata)  # We get a @property decorated method!


DefaultAddForm.additionalSchemata = patched_additionalSchemata()
