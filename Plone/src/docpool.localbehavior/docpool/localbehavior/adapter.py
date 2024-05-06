from docpool.base.appregistry import BEHAVIOR_REGISTRY
from docpool.base.content.dpdocument import IDPDocument
from docpool.base.interfaces import IExtension
from docpool.localbehavior.localbehavior import ILocalBehaviorSupporting
from plone.dexterity.behavior import DexterityBehaviorAssignable
from plone.dexterity.schema import SCHEMA_CACHE
from plone.uuid.interfaces import IUUID
from zope.component import adapter
from zope.component import getMultiAdapter

import six


@adapter(ILocalBehaviorSupporting)
class DexterityLocalBehaviorAssignable(DexterityBehaviorAssignable):

    def enumerateBehaviors(self):
        request = self.context.REQUEST
        if isinstance(request, six.string_types):
            # Shortcut when Request is '<Special Object Used to Force Acquisition>'
            raise StopIteration
        edited_behaviors = request.get(
            "form.widgets.ILocalBehaviorSupport.local_behaviors", []
        )
        edited_behaviors = set(edited_behaviors)

        # Here we save the behaviors saved previously in the context in the request,
        # because we will need to check this list later
        # and it might be changed during a "save"
        uuid = IUUID(self.context, None)
        cachekey = "savedLocalBehaviors_for_{}".format(uuid)
        saved_behaviors = request.get(cachekey, [])
        if uuid and not saved_behaviors:
            saved_behaviors = getattr(self.context, 'local_behaviors', [])[:]
            request.set(cachekey, saved_behaviors)
        edited_behaviors.update(saved_behaviors)

        if IDPDocument.providedBy(self.context):
            dp_app_state = getMultiAdapter(
                (self.context, request), name=u'dp_app_state'
            )
            available_apps = dp_app_state.appsEffectiveForObject(request)
        else:
            available_apps = getattr(self.context, 'local_behaviors', [])
        edited_behaviors.update(available_apps)

        for behavior in SCHEMA_CACHE.behavior_registrations(
                self.context.portal_type):
            if isSupported(edited_behaviors, behavior.interface):
                yield behavior


def isSupported(available_apps, behavior_interface):
    if behavior_interface.extends(IExtension):
        if available_apps:
            return set(
                BEHAVIOR_REGISTRY.get(behavior_interface.__identifier__)
            ).intersection(available_apps)
        else:
            return False
    else:
        return True
