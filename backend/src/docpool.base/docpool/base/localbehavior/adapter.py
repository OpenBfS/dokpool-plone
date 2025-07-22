from Acquisition import aq_get
from docpool.base.appregistry import BEHAVIOR_REGISTRY
from docpool.base.localbehavior.localbehavior import ILocalBehaviorSupporting
from plone.dexterity.behavior import DexterityBehaviorAssignable
from plone.dexterity.schema import SCHEMA_CACHE
from plone.uuid.interfaces import IUUID
from zope.component import adapter
from zope.component import getMultiAdapter


@adapter(ILocalBehaviorSupporting)
class DexterityLocalBehaviorAssignable(DexterityBehaviorAssignable):
    """Adapter that provides dynamic behavior enumeration for local behavior supporting content.

    This adapter extends Plone's standard behavior assignment mechanism to support
    object-based (local) behaviors in addition to type-based behaviors. It determines
    which behaviors should be active for a specific content object based on:

    1. The object's assigned local_behaviors (stored on the object)
    2. Form data during editing (temporary behavior assignment)
    3. Available applications in the current DocumentPool context
    4. The object's doctype configuration (for DPDocuments)

    This enables the core Dokpool functionality where the same content type
    (DPDocument) can have different behaviors, fields, and views depending on
    which applications (ELAN, REI, RODOS, DOKSYS) it's assigned to.
    """

    def enumerateBehaviors(self):
        """Enumerate all behaviors that should be active for this content object.

        This method determines which behaviors should be applied by combining:
        - Behaviors being edited in the current form
        - Previously saved behaviors on the object
        - Available applications in the current context

        The method caches previously saved behaviors in the request to handle
        cases where behaviors might change during form processing.

        Yields:
            BehaviorRegistration: Each behavior that should be active for this object
        """
        request = aq_get(self.context, "REQUEST", None)
        if not request or isinstance(request, str):
            # Shortcut when Request is '<Special Object Used to Force Acquisition>'
            return
        edited_behaviors = request.get("form.widgets.ILocalBehaviorSupport.local_behaviors", [])
        edited_behaviors = set(edited_behaviors)

        local_behaviors = getattr(self.context, "local_behaviors", [])

        # Here we save the behaviors saved previously in the context in the request,
        # because we will need to check this list later
        # and it might be changed during a "save"
        uuid = IUUID(self.context, None)
        if uuid:
            cachekey = "savedLocalBehaviors"
            cache = request.get(cachekey, {})
            if not cache:
                request.set(cachekey, cache)
            saved_behaviors = cache.setdefault(uuid, local_behaviors[:])
        else:
            saved_behaviors = local_behaviors
        edited_behaviors.update(saved_behaviors)

        from docpool.base.content.dpdocument import IDPDocument

        if IDPDocument.providedBy(self.context):
            dp_app_state = getMultiAdapter((self.context, request), name="dp_app_state")
            available_apps = dp_app_state.appsEffectiveForObject(request)
        else:
            available_apps = local_behaviors
        edited_behaviors.update(available_apps)

        for behavior in SCHEMA_CACHE.behavior_registrations(self.context.portal_type):
            if isSupported(edited_behaviors, behavior.interface):
                yield behavior


def isSupported(available_apps, behavior_interface):
    """Check if a behavior interface is supported given the available applications.

    This function determines whether a specific behavior should be active based on:
    - Whether it's an IExtension behavior (app-specific) or core behavior
    - Which applications are currently available/active
    - The behavior's registration in the BEHAVIOR_REGISTRY

    Args:
        available_apps (list): List of application identifiers that are available
                              (e.g., ['elan', 'rei'])
        behavior_interface (Interface): The behavior interface to check

    Returns:
        bool or set: True if supported (for non-extension behaviors),
                    set intersection if extension behavior matches available apps,
                    False if extension behavior with no available apps
    """
    from docpool.base.interfaces import IExtension

    if behavior_interface.extends(IExtension):
        if available_apps:
            return set(BEHAVIOR_REGISTRY.get(behavior_interface.__identifier__, [])).intersection(
                available_apps
            )
        else:
            return False
    else:
        return True
