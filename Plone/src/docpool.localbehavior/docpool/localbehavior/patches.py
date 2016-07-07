from plone.dexterity.schema import SCHEMA_CACHE
from zope.interface.declarations import getObjectSpecification
from zope.interface.declarations import implementedBy
from zope.interface.declarations import Implements
from docpool.base.appregistry import extensionFor

def patch_fti_localbehavior():
    from plone.dexterity.content import FTIAwareSpecification

    if getattr(FTIAwareSpecification, '__localbehavior_patched', False):
        return

    from plone.behavior.interfaces import IBehaviorAssignable
    from plone.behavior.interfaces import IBehavior
    from zope.component import queryUtility

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
            hash(direct_spec)
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
                        #print behavior_registration.marker
                        dynamically_provided.append(
                            behavior_registration.marker
                        )

            # DOCPOOL: this is the new part!
            for name in (getattr(inst, 'local_behaviors', []) or []):
                print "getting local behavior ", name
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
            inst._v__providedBy__ = updated + (None, )
            return spec

        dynamically_provided.append(spec)
        all_spec = Implements(*dynamically_provided)
        inst._v__providedBy__ = updated + (all_spec, )
        return all_spec

    FTIAwareSpecification.__get__ = __get__
    FTIAwareSpecification.__localbehavior_patched = True

# patch_fti_localbehavior()
