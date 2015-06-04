# -*- coding: utf-8 -*-
#
# File: elandoccollection.py
#
# Copyright (c) 2015 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

"""Define a browser view for the content type. In the FTI 
configured in profiles/default/types/*.xml, this is being set as the default
view of that content type.
"""


from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone.memoize.instance import memoize

##code-section imports
from elan.esd.utils import getAvailableCategories, getCategoriesForCurrentUser
from elan.esd.browser.viewlets.common import ScenarioViewlet
from Products.CMFCore.utils import getToolByName
##/code-section imports

class ELANDocCollectionView(BrowserView):
    """Default view
    """
 
    __call__ = ViewPageTemplateFile('elandoccollection.pt')
   
    ##code-section methods1
    ##/code-section methods1     

class ELANDocCollectionrpopupView(BrowserView):
    """Additional View
    """
    
    __call__ = ViewPageTemplateFile('elandoccollectionrpopup.pt')
    
    ##code-section methodsrpopup
    def selected_categories(self):
        """
        """
        return getCategoriesForCurrentUser(self.context)
    
    def available_categories(self):
        """
        """
        return getAvailableCategories(self.context)
    
    def scenario_view(self):
        """
        """
        v = ScenarioViewlet(self.context, self.request, self)
        v.update()
        return v
    ##/code-section methodsrpopup     



##code-section bottom
class ELANDocCollectionDocView(BrowserView):
    """Default view
    """
 
    __call__ = ViewPageTemplateFile('elandoccollectiondoc.pt')
    
    def doc(self):
        """
        Return the elan document, which is to be viewed in the context of the collection.
        """
        uid = self.request.get("d", None)
        if uid:
            catalog = getToolByName(self, 'portal_catalog')
            result  = catalog({'UID' : uid})
            if len(result) == 1:
                o = result[0].getObject()
                return o
        return None
   
##/code-section bottom