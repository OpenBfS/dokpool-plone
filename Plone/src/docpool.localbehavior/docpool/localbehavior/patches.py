from docpool.base.appregistry import extensionFor
from docpool.localbehavior.adapter import isSupported
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.schema import SCHEMA_CACHE
from zope.component import getMultiAdapter
from zope.interface.declarations import getObjectSpecification
from zope.interface.declarations import implementedBy
from zope.interface.declarations import Implements

import logging


log = logging.getLogger("docpool.localbehavior")


def patch_fti_localbehavior():
    from plone.dexterity.content import FTIAwareSpecification

    if getattr(FTIAwareSpecification, '__localbehavior_patched', False):
        return

    from plone.behavior.interfaces import IBehaviorAssignable

    _orig_get = FTIAwareSpecification.__get__

    def __get__(self, inst, cls=None):
        # We're looking at a class - fall back on default
        if inst is None:
            return getObjectSpecification(cls)

        direct_spec = getattr(inst, '__provides__', None)

        # avoid recursion - fall back on default
        if getattr(self, '__recursion__', False):
            return direct_spec

        spec = direct_spec

        # If the instance doesn't have a __provides__ attribute, get the
        # interfaces implied by the class as a starting point.
        if spec is None:
            spec = implementedBy(cls)

        # Find the data we need to know if our cache needs to be invalidated
        portal_type = getattr(inst, 'portal_type', None)

        # If the instance has no portal type, then we're done.
        if portal_type is None:
            return spec

        # Find the cached value. This calculation is expensive and called
        # hundreds of times during each request, so we require a fast cache
        cache = getattr(inst, '_v__providedBy__', None)

        # See if we have a current cache. Reasons to do this include:
        #
        #  - The FTI was modified.
        #  - The instance was modified and persisted since the cache was built.
        #  - The instance has a different direct specification.
        updated = (
            inst._p_mtime,
            SCHEMA_CACHE.modified(portal_type),
            SCHEMA_CACHE.invalidations,
            hash(direct_spec),
        )
        if cache is not None and cache[:-1] == updated:
            if cache[-1] is not None:
                return cache[-1]
            return spec

        main_schema = SCHEMA_CACHE.get(portal_type)
        if main_schema:
            dynamically_provided = [main_schema]
        else:
            dynamically_provided = []

        # block recursion
        self.__recursion__ = True
        try:
            assignable = IBehaviorAssignable(inst, None)
            if assignable is not None:
                for behavior_registration in assignable.enumerateBehaviors():
                    if behavior_registration.marker:
                        # print behavior_registration.marker
                        dynamically_provided.append(
                            behavior_registration.marker)

            # DOCPOOL: this is the new part!
            for name in getattr(inst, 'local_behaviors', []) or []:
                # print "getting local behavior ", name
                dynamically_provided.append(extensionFor(inst, name))
        #                behavior = extensionFor(inst, name)
        #                print behavior
        #                if behavior.marker is not None:
        #                    print behavior.marker
        #                    dynamically_provided.append(behavior.marker)

        finally:
            del self.__recursion__

        if not dynamically_provided:
            # rare case if no schema nor behaviors with markers are set
            inst._v__providedBy__ = updated + (None,)
            return spec

        dynamically_provided.append(spec)
        all_spec = Implements(*dynamically_provided)
        inst._v__providedBy__ = updated + (all_spec,)
        return all_spec

    FTIAwareSpecification.__get__ = __get__
    FTIAwareSpecification.__localbehavior_patched = True


# patch_fti_localbehavior()


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
    log.debug(
        "getAdditionalSchemata with context %r and portal_type %s", context, portal_type
    )
    # Usually an add-form.
    if portal_type is None:
        portal_type = context.portal_type

    # DOCPOOL modification! We only want to see behaviors that are allowed
    # here.
    dp_app_state = getMultiAdapter((context, request), name='dp_app_state')
    available_apps = dp_app_state.appsPermittedForObject(context.REQUEST)
    activated_apps = dp_app_state.appsActivatedByCurrentUser()
    effective_apps = list(
        set(available_apps).intersection(
            set(activated_apps)))

    for schema_interface in SCHEMA_CACHE.behavior_schema_interfaces(
            portal_type):
        if isSupported(effective_apps, schema_interface):
            form_schema = IFormFieldProvider(schema_interface, None)
            if form_schema is not None:
                yield form_schema


def patched_additionalSchemata():
    return property(additionalSchemata)  # We get a @property decorated method!


setattr(DefaultAddForm, "additionalSchemata", patched_additionalSchemata())
