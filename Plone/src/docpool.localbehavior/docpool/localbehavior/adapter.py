from zope.interface import implements
from zope.component import adapts, getUtility, queryUtility
from plone.dexterity.schema import SCHEMA_CACHE

from plone.dexterity.behavior import DexterityBehaviorAssignable

from docpool.base.appregistry import BEHAVIOR_REGISTRY
from docpool.base.content.dpdocument import IDPDocument
from docpool.localbehavior.localbehavior import (
    ILocalBehaviorSupporting,
    ILocalBehaviorSupport,
)
from docpool.base.interfaces import IExtension
from zope.component import getMultiAdapter


class DexterityLocalBehaviorAssignable(DexterityBehaviorAssignable):
    adapts(ILocalBehaviorSupporting)

    def __init__(self, context):
        super(DexterityLocalBehaviorAssignable, self).__init__(context)
        self.context = context

    def enumerateBehaviors(self):
        # print "enumerate"
        request = self.context.REQUEST
        editedLocalBehaviours = []
        try:
            editedLocalBehaviours = request.get(
                "form.widgets.ILocalBehaviorSupport.local_behaviors", []
            )
        except:
            pass
        editedLocalBehaviours = list(set(editedLocalBehaviours))
        # print "edited", editedLocalBehaviours

        # Here we save the behaviors saved previously in the context in the request,
        # because we will need to check this list later
        # and it might be changed during a "save"
        if not request.get("savedLocalBehaviors", []):
            savedBehaviors = getattr(self.context, 'local_behaviors', [])[:]
            request.set("savedLocalBehaviors", list(set(savedBehaviors)))
            # print "saved", savedBehaviors

        if IDPDocument.providedBy(self.context):
            dp_app_state = getMultiAdapter(
                (self.context, request), name=u'dp_app_state'
            )
            self.available_apps = dp_app_state.appsEffectiveForObject(request)
        #            self.available_apps = list(set(self.available_apps).intersection(getattr(self.context, 'local_behaviors', [])))
        else:
            self.available_apps = list(
                set(getattr(self.context, 'local_behaviors', [])[:])
            )

        editedLocalBehaviours.extend(self.available_apps)
        editedLocalBehaviours.extend(request.get("savedLocalBehaviors", []))
        editedLocalBehaviours = list(set(editedLocalBehaviours))
        # print "resulting", editedLocalBehaviours

        # print "enumerate ", self.available_apps
        for behavior in SCHEMA_CACHE.behavior_registrations(self.context.portal_type):
            if isSupported(editedLocalBehaviours, behavior.interface):
                yield behavior


def isSupported(available_apps, behavior_interface):
    if behavior_interface.extends(IExtension):
        if available_apps:
            return set(
                BEHAVIOR_REGISTRY.get(behavior_interface.__identifier__)
            ).intersection(set(available_apps))
        else:
            return False
    else:
        return True
