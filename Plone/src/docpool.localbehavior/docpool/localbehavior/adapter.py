# -*- coding: utf-8 -*- 
from zope.interface import implements
from zope.component import adapts, getUtility, queryUtility
from plone.dexterity.schema import SCHEMA_CACHE

from plone.dexterity.behavior import DexterityBehaviorAssignable

from docpool.base.appregistry import BEHAVIOR_REGISTRY
from docpool.base.content.dpdocument import IDPDocument
from docpool.localbehavior.localbehavior import ILocalBehaviorSupporting, ILocalBehaviorSupport
from docpool.base.interfaces import IExtension
from zope.component import getMultiAdapter

class DexterityLocalBehaviorAssignable(DexterityBehaviorAssignable):
    adapts(ILocalBehaviorSupporting)

    def __init__(self, context):
        super(DexterityLocalBehaviorAssignable, self).__init__(context)
        self.context = context

    def enumerateBehaviors(self):
        #print "enumerate"
        request = self.context.REQUEST

        isInit = request.get("form.buttons.save", None)

        if IDPDocument.providedBy(self.context):
            dp_app_state = getMultiAdapter((self.context, request), name=u'dp_app_state')
            self.available_apps = dp_app_state.appsEffectiveForObject(request)
#            self.available_apps = list(set(self.available_apps).intersection(getattr(self.context, 'local_behaviors', [])))
        else:
            self.available_apps = getattr(self.context, 'local_behaviors', [])

        #print "enumerate ", self.available_apps
        for behavior in SCHEMA_CACHE.behavior_registrations(
            self.context.portal_type
        ):
            if isInit or isSupported(self.available_apps, behavior.interface):
                yield behavior

def isSupported(available_apps, behavior_interface):
    if behavior_interface.extends(IExtension):
        if available_apps:
            return set(BEHAVIOR_REGISTRY.get(behavior_interface.__identifier__)).intersection(set(available_apps))
        else:
            return False
    else:
        return True