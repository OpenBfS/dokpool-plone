from AccessControl.SecurityInfo import allow_module
from docpool.base.content.archiving import IArchiving
from docpool.elan.config import ELAN_APP
from docpool.elan.utils import getOpenScenarios
from docpool.elan.utils import getScenariosForCurrentUser
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter


allow_module("docpool.elan.browser")
allow_module("docpool.elan.browser.viewlets")
allow_module("docpool.elan.browser.viewlets.common")


class EventViewlet(ViewletBase):
    index = ViewPageTemplateFile("events.pt")

    def isSupported(self):
        dp_app_state = getMultiAdapter(
            (self.context, self.request), name="dp_app_state"
        )
        return dp_app_state.isCurrentlyActive(ELAN_APP)

    @property
    def available(self):
        return hasattr(self.context, "myDocumentPool") and self.isSupported()

    def update(self):
        scs = getOpenScenarios(self.context)
        self.scenarios = [s.getObject() for s in scs if s.review_state == "published"]
        self.open_scenarios = [s.getObject() for s in scs]
        scs = getScenariosForCurrentUser()
        self.selected_scenarios = scs


class ELANViewlet(ViewletBase):
    def isSupported(self):
        dp_app_state = getMultiAdapter(
            (self.context, self.request), name="dp_app_state"
        )
        return dp_app_state.isCurrentlyActive(ELAN_APP)


class TickerViewlet(ELANViewlet):
    index = ViewPageTemplateFile("ticker.pt")

    @property
    def available(self):
        return (
            not IArchiving(self.context).is_archive
            and hasattr(self.context, "myDocumentPool")
            and self.isSupported()
        )
