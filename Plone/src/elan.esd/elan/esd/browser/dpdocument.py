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
from Acquisition import aq_inner
import urllib
from datetime import datetime
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from plone.app.layout.globals.interfaces import IViewView
from zope.interface import implements
from zope.interface import alsoProvides
from base64 import b64encode
from plone.protect.authenticator import createToken
from elan.esd.behaviors.elandocument import IELANDocument
##/code-section imports

class DPDocumentView(BrowserView):
    """Default view
    """
 
    __call__ = ViewPageTemplateFile('dpdocument.pt')
   
    ##code-section methods1
    def base_url(self):
        """
        """
        context = aq_inner(self.context)
        return context.restrictedTraverse('@@plone').getCurrentFolderUrl()
    
    def getUploadUrl(self):
        """
        return upload url
        in current folder
        """
        folder_url = self.base_url()
        return '%s/@@quick_upload' %folder_url

    def getDataForUploadUrl(self):
        data_url = ''
        return data_url

    def elanobject(self):
        return IELANDocument(self.context)

    def javascript(self):
        # PLONE5: plone.protect verlangt CSRF Tokens im Request :-)
        token = createToken()
        return """
  // workaround this MSIE bug :
  // https://dev.plone.org/plone/ticket/10894
  if (navigator.userAgent.match(/msie|trident/i)) jQuery("#settings").remove();
  var Browser = {};
  Browser.onUploadComplete = function() {
      window.location.reload();
  }
  loadUploader = function() {
      var ulContainer = jQuery('.elanUploaderContainer');
      ulContainer.each(function(){
          var uploadUrl =  jQuery('.uploadUrl', this).val();
          var uploadData =  jQuery('.uploadData', this).val();
          var UlDiv = jQuery(this);
          jQuery.ajax({
                     type: 'GET',
                     url: uploadUrl,
                     data: uploadData,
                     dataType: 'html',
                     contentType: 'text/html; charset=utf-8',
                     headers: { 'X-CSRF-TOKEN': '%s' },
                     success: function(html) {
                        UlDiv.html(html);
                     } });
      });
  }
  jQuery(document).ready(loadUploader);
""" % token

    def quote_plus(self, string):
        """
        """
        return urllib.quote_plus(string)
    ##/code-section methods1     

class DPDocumentinlineView(BrowserView):
    """Additional View
    """
    
    __call__ = ViewPageTemplateFile('dpdocumentinline.pt')
    
    ##code-section methodsinline
    implements(IViewView)
        
    def elanobject(self):
        return IELANDocument(self.context)
    ##/code-section methodsinline     

class DPDocumentlistitemView(BrowserView):
    """Additional View
    """
    
    __call__ = ViewPageTemplateFile('dpdocumentlistitem.pt')
    
    ##code-section methodslistitem
    def ctype_short(self, file):
        """
        """
        # print file
        ctype = str(file.file.contentType)
        s = ctype.split('/')
        if len(s) == 2:
            return s[1]
        else:
            return s[0]
        
    def elanobject(self):
        return IELANDocument(self.context)
    ##/code-section methodslistitem     



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
        return IELANDocument(self.context)

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
        return b64encode(file.index_html())
        
    
##/code-section bottom