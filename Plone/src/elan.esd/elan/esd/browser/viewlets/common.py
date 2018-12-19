from zope.component import getMultiAdapter
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.Archetypes.utils import shasattr
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import base_hasattr, parent, safe_hasattr

from docpool.elan.config import ELAN_APP
from docpool.event.utils import getActiveScenarios, getOpenScenarios, getScenariosForCurrentUser
from AccessControl.SecurityInfo import allow_module, allow_class

allow_module("elan.esd.browser");
allow_module("elan.esd.browser.viewlets");
allow_module("elan.esd.browser.viewlets.common");


class ELANViewlet(ViewletBase):
    def isSupported(self):
        dp_app_state = getMultiAdapter((self.context, self.request), name=u'dp_app_state')
        return dp_app_state.isCurrentlyActive(ELAN_APP)


class TickerViewlet(ELANViewlet):
    index = ViewPageTemplateFile('ticker.pt')
    
    @property
    def available(self):
        return (not self.context.isArchive()) and self.context.isSituationDisplay() and self.isSupported()
        
    