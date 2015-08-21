from plone.app.layout.viewlets.common import GlobalSectionsViewlet as GSV, ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from AccessControl.SecurityInfo import allow_module, allow_class

allow_module("elan.esd.browser");
allow_module("elan.esd.browser.viewlets");
allow_module("elan.esd.browser.viewlets.common");

class GlobalSectionsViewlet(GSV):
    index = ViewPageTemplateFile('sections.pt')
    
    def update(self):
        GSV.update(self)
        
class TimeViewlet(ViewletBase):
    index = ViewPageTemplateFile('time.pt')
    
allow_class(TimeViewlet)
        
    