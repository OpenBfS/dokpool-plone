from AccessControl.SecurityInfo import allow_module
from docpool.event.utils import getOpenScenarios
from docpool.event.utils import getScenariosForCurrentUser
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


allow_module("docpool.event.browser")
allow_module("docpool.event.browser.viewlets")
allow_module("docpool.event.browser.viewlets.common")


class EventViewlet(ViewletBase):
    index = ViewPageTemplateFile("events.pt")

    def isSupported(self):
        return True

    @property
    def available(self):
        return self.context.isSituationDisplay() and self.isSupported()

    def update(self):
        scs = getOpenScenarios(self.context)
        self.scenarios = [s.getObject() for s in scs if s.review_state == "published"]
        self.open_scenarios = [s.getObject() for s in scs]
        scs = getScenariosForCurrentUser(self.context)
        self.selected_scenarios = scs
