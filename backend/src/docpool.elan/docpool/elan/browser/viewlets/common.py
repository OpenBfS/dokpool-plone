from AccessControl.SecurityInfo import allow_module
from Acquisition import aq_get
from docpool.base.content.archiving import IArchiving
from docpool.base.content.places import IPlaces
from docpool.elan.config import ELAN_APP
from docpool.elan.utils import getOpenScenarios
from docpool.elan.utils import getScenariosForCurrentUser
from plone import api
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter


allow_module("docpool.elan.browser")
allow_module("docpool.elan.browser.viewlets")
allow_module("docpool.elan.browser.viewlets.common")


class ELANViewlet(ViewletBase):
    def isSupported(self):
        dp_app_state = getMultiAdapter((self.context, self.request), name="dp_app_state")
        return dp_app_state.isCurrentlyActive(ELAN_APP)

    @property
    def available(self):
        return IPlaces(self.context).document_pool is not None and self.isSupported()


# TODO Remove once the new GUI is finished
class EventViewlet(ELANViewlet):
    index = ViewPageTemplateFile("events.pt")

    def update(self):
        scs = getOpenScenarios(self.context)
        self.scenarios = [(s.UID, s.getObject()) for s in scs if s.review_state == "published"]
        scs = getScenariosForCurrentUser()
        possible_uids = {s[0] for s in self.scenarios}
        self.selected_scenarios = [s for s in scs if s in possible_uids]
        self.archive_url = (
            IPlaces(self.context).document_pool.archive.absolute_url()
            if "archive" in self.context.getPhysicalPath()
            else None
        )

    def number_of_entries(self, dpevent):
        contentarea = aq_get(dpevent, "content")
        args = {
            "portal_type": "DPDocument",
            "scenario": dpevent.UID(),
        }
        return len(api.content.find(context=contentarea, **args))


class TickerViewlet(ELANViewlet):
    index = ViewPageTemplateFile("ticker.pt")

    @property
    def available(self):
        return not IArchiving(self.context).is_archive and super().available

    def ticker(self):
        # Contentconfig not not accessible to Reader role but we need to access the ticker
        contentconfig = self.context.unrestrictedTraverse("contentconfig")
        if contentconfig and "ticker" in contentconfig:
            return contentconfig["ticker"]
