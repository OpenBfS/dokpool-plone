# -*- coding: utf-8 -*-
#
# File: srmodule.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
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
from docpool.elan.config import ELAN_APP
##/code-section imports

class SRModuleView(BrowserView):
    """Default view
    """
 
    __call__ = ViewPageTemplateFile('srmodule.pt')
   
    ##code-section methods1
    def elanobject(self):
        return self.context.doc_extension(ELAN_APP)
    ##/code-section methods1     

class SRModulematerialView(BrowserView):
    """Additional View
    """
    
    __call__ = ViewPageTemplateFile('srmodulematerial.pt')
    
    ##code-section methodsmaterial
    def elanobject(self):
        return self.context.doc_extension(ELAN_APP)
    ##/code-section methodsmaterial     

class SRModuleinfoView(BrowserView):
    """Additional View
    """
    
    __call__ = ViewPageTemplateFile('srmoduleinfo.pt')
    
    ##code-section methodsinfo
    def elanobject(self):
        return self.context.doc_extension(ELAN_APP)
    ##/code-section methodsinfo     



##code-section bottom
##/code-section bottom