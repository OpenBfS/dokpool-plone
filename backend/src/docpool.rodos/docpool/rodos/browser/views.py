from docpool.base import DocpoolMessageFactory as _
from docpool.base.localbehavior.localbehavior import ILocalBehaviorSupport
from docpool.elan.behaviors.elandocument import IELANDocument
from docpool.elan.config import ELAN_APP
from docpool.elan.utils import getOpenScenarios
from docpool.elan.utils import getScenariosForCurrentUser
from docpool.rodos.behaviors.rodosdoc import IRodosDoc
from plone import api
from Products.Five import BrowserView
from zope.i18nmessageid import MessageFactory

PMF = MessageFactory("plone")


class AssignToElanEvent(BrowserView):

    def __call__(self):
        form = self.request.form
        obj = self.context
        if IELANDocument(obj, None):
            msg = _("This is already a ELAN document.")
            api.portal.show_message(msg, self.request)
            return self.request.response.redirect(obj.absolute_url())

        dpevents = getOpenScenarios(obj)
        self.events = [i for i in dpevents if i.review_state == "published"]
        self.current_event = None

        if current_event := getScenariosForCurrentUser():
            current_event_id = current_event[0]
            for brain in self.events:
                if brain.id == current_event_id:
                    self.current_event = brain.id
                    break

        if form.get("form.button.cancel"):
            msg = PMF("Changes canceled.")
            api.portal.show_message(msg, self.request)
            return self.request.response.redirect(obj.absolute_url())

        if not form.get("form.button.submit"):
            return self.index()

        self.event_uid = form.get("dpevent", "")

        # Enable ELAN local behavior
        adapted = ILocalBehaviorSupport(obj)
        apps = adapted.local_behaviors
        apps.append(ELAN_APP)
        adapted.local_behaviors = list(set(apps))

        # Assign to event
        obj.doc_extension(ELAN_APP).scenarios = self.event_uid
        obj.reindexObject(idxs=["apps_supported", "scenarios"])

        msg = _("Assigned to ELAN event")
        api.portal.show_message(msg, self.request)
        return self.request.response.redirect(obj.absolute_url())


class CanAssignToElanEvent(BrowserView):

    def __call__(self):
        obj = self.context
        if IELANDocument(obj, None):
            return False

        if not IRodosDoc(obj, None):
            return False

        return True
