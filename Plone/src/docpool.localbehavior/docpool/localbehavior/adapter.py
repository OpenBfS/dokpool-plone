from zope.interface import implements
from zope.component import adapts, getUtility, queryUtility
from plone.dexterity.schema import SCHEMA_CACHE

from plone.dexterity.behavior import DexterityBehaviorAssignable

from docpool.base.appregistry import BEHAVIOR_REGISTRY
from docpool.localbehavior.localbehavior import ILocalBehaviorSupporting, ILocalBehaviorSupport
from docpool.base.interfaces import IExtension
class DexterityLocalBehaviorAssignable(DexterityBehaviorAssignable):
    adapts(ILocalBehaviorSupporting)

    def __init__(self, context):
        super(DexterityLocalBehaviorAssignable, self).__init__(context)
        self.context = context

    def enumerateBehaviors(self):
        #print "enumerate"
        isFormSubmit = self.context.REQUEST.get("form.buttons.save", None)

        self.local_behaviors = getattr(self.context, 'local_behaviors', [])
        for behavior in SCHEMA_CACHE.behavior_registrations(
            self.context.portal_type
        ):
            if isFormSubmit or self.isSupported(behavior):
                yield behavior

    def isSupported(self, behaviour):
        if behaviour.interface.extends(IExtension):
            if self.local_behaviors:
                return set(BEHAVIOR_REGISTRY.get(behaviour.interface.__identifier__)).intersection(set(self.local_behaviors))
            else:
                return False
        else:
            return True