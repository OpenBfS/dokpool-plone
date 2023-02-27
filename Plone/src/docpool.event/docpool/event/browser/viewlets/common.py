from AccessControl.SecurityInfo import allow_module
from docpool.event.utils import getOpenScenarios
from docpool.event.utils import getScenariosForCurrentUser
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


allow_module("docpool.event.browser")
allow_module("docpool.event.browser.viewlets")
allow_module("docpool.event.browser.viewlets.common")


class EventViewlet(ViewletBase):
    index = ViewPageTemplateFile('events.pt')

    def isSupported(self):
        return True

    @property
    def available(self):
        return self.context.isSituationDisplay() and self.isSupported()

    def update(self):
        scs = getOpenScenarios(self.context)
        scs = [s for s in scs if s.review_state == 'published']
        self.scenarios = [(s.UID, s.getObject()) for s in scs]
        possible_ids = set(s.UID for s in scs)
        self.selected_scenarios = [
            s for s in getScenariosForCurrentUser(self.context) if s in possible_ids
        ]
