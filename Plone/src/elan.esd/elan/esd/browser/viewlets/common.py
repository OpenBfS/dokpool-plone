from zope.component import getMultiAdapter
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Archetypes.utils import shasattr
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import base_hasattr, parent, safe_hasattr
from elan.esd.utils import getActiveScenarios, getOpenScenarios, getScenariosForCurrentUser
from AccessControl.SecurityInfo import allow_module, allow_class

allow_module("elan.esd.browser");
allow_module("elan.esd.browser.viewlets");
allow_module("elan.esd.browser.viewlets.common");

class ScenarioViewlet(ViewletBase):
    index = ViewPageTemplateFile('scenarios.pt')
    
    def update(self):
        scs = getOpenScenarios(self.context)
        self.scenarios = [ s.getObject() for s in scs if s.review_state == 'published' ]
        self.open_scenarios = [ s.getObject() for s in scs ]
        scs = getScenariosForCurrentUser(self.context)
        self.selected_scenarios = scs
        
class TimeViewlet(ViewletBase):
    index = ViewPageTemplateFile('time.pt')
    
allow_class(TimeViewlet)
        
    