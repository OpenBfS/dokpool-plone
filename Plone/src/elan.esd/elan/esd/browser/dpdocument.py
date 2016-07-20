# -*- coding: utf-8 -*-
#
# File: dpdocument.py
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
from docpool.elan.config import ELAN_APP
from base64 import b64encode
from datetime import datetime
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
##/code-section imports


##code-section bottom
class DPDocumentirixView(BrowserView):
    """Additional View
    """
    
    __call__ = ViewPageTemplateFile('dpdocumentirix.pt')
    
    ##code-section methodsirix
    
    def __init__(self, context, request):
        BrowserView.__init__(self,context,request)
        self.ic = self.irixConfig()
        
    def elanobject(self):
        return self.context.doc_extension(ELAN_APP)

    def filename(self):
        """
        """
        return "%s.xml" % self.context.getId()
        
    def irixConfig(self):
        try:
            ic = self.context.contentconfig.irix
            return ic
        except:
            return None
        
    def timestamp(self):
        date = datetime.utcnow()
        return date.strftime("%Y-%m-%dT%H:%M:%SZ")
    
    def scenario(self):
        try:
            scns = self.context.scenarios
            if scns:
                scn = scns[0]
                # We can't search the catalog for the title directly...
                cat = getToolByName(self.context, "portal_catalog")
                all_scns = cat(portal_type='ELANScenario')
                for s in all_scns:
                    if s.Title == scn:
                        return s.getObject()
        except:
            pass
        return None
    
    def scenarioType(self):
        """
        """
        scen = self.scenario()
        if scen:
            if scen.exercise:
                return "Exercise"
            else:
                return "Emergency"
        return "Unknown"
        
    def scenarioTime(self):
        """
        """
        scen = self.scenario()
        if scen:
            dt = scen.timeOfEvent
            return dt.strftime("%Y-%m-%dT%H:%M:%SZ")
        return self.timestamp()
    
    def mtime(self):
        """
        """
        return self.context.mdate and self.context.mdate.strftime("%Y-%m-%dT%H:%M:%SZ") or ""
    
    def attachments(self):
        """
        """
        return self.context.getFiles()
            
    def docText(self):
        """
        """
        d = self.context.Description()
        t = self.context.Title()
        txt = self.context.text and self.context.text.output.encode('utf-8') or ''
        return "%s - %s: %s" % (d, t, txt)
        
    def irixType(self):
        """
        """
        mapping = self.ic.typeMapping
        et = self.context.dp_type_name()
        for line in eval(str(mapping)):
            parts = line.split(":")
            if parts[0] == et:
                return parts[1]
        return "Unknown"
    
    def isEventDescription(self):
        """
        """
        return self.irixType() in ['Event information', 'Public information', 'Public information - Press release']
    
    def isActualRelease(self):
        """
        """
        return self.irixType() in ['Plant status']
    
    def isMeteoInfo(self):
        """
        """
        return self.irixType() in ['Meteorology', 'Model result - Plume trajectory']
    
    def isFutureRelease(self):
        """
        """
        return self.irixType() in ['Model result']
    
    def isMeasurements(self):
        """
        """
        return (self.irixType() in ['Measurements']) and (self.context.dp_type_name() != 'Gamma Dose Rate')
    
    def isProtectiveActions(self):
        """
        """
        return self.irixType() in ['Protective actions']
    
    def isDoseRate(self):
        """
        """
        return self.context.dp_type_name() in ['Gamma Dose Rate']
    
    def base64(self, file):
        """
        """
        return b64encode(file.index_html().encode('utf-8'))
        
    
##/code-section bottom