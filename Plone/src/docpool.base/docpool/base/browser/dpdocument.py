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
from Acquisition import aq_inner, aq_base, ImplicitAcquisitionWrapper
import urllib
from plone.app.layout.globals.interfaces import IViewView
from zope.interface import implements
from zope.interface import alsoProvides
from plone.protect.authenticator import createToken
from Products.Archetypes.utils import shasattr, contentDispositionHeader
from plone.app.contenttypes.interfaces import IFile
from zope.pagetemplate.interfaces import IPageTemplateSubclassing
from Products.PageTemplates.PageTemplate import PageTemplate
from plone.protect.interfaces import IDisableCSRFProtection
from docpool.base.utils import execute_under_special_role
from docpool.base.content.dpdocument import DPDocument
import Acquisition
##/code-section imports

class OnTheFlyTemplate(Acquisition.Explicit, PageTemplate):
    pass

class FlexibleView(BrowserView):
    __allow_access_to_unprotected_subobjects__ = 1

    def myViewSource(self, vtype):
        """
        """
        doc = self.context
        dto = doc.docTypeObj()
        app = doc.currentApplication()
        dtid = dto.getId()
        data = ""
        
        for n in [
                  "%s_doc_%s_%s" % (app, dtid, vtype),
                  "%s_doc_%s" % (app, vtype),
                  "doc_%s_%s" % (dtid, vtype),
                  "doc_%s" % vtype
                  ]:
            if shasattr(dto, n, acquire=True):
                o = aq_base(getattr(dto, n))
                if IFile.providedBy(o):
                    f = o.file.open()
                    data = f.read()
                elif IPageTemplateSubclassing.providedBy(o):
                    data = o.read()
                return data
        return data

    def myView(self, vtype, **options):
        """
        """
        src = self.myViewSource(vtype)
        template = OnTheFlyTemplate()
        template = template.__of__(aq_base(self.context))
        template.pt_edit(src, "text/html")
#        template.id = "flexible"
        # This "view" will run with security restrictions. The code will not be able
        # to access protected attributes and functions.
        # BUT: code included via macros works!
        return template(view=self, context=self.context, request=self.request, **options)

class DPDocumentView(FlexibleView):
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

    def javascript(self):
        # PLONE5: plone.protect 
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

class DPDocumentlistitemView(FlexibleView):
    """Additional View
    """
    __allow_access_to_unprotected_subobjects__ = 1
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
        
    ##/code-section methodslistitem     

class DPDocumentinlineView(FlexibleView):
    """Additional View
    """
    
    __call__ = ViewPageTemplateFile('dpdocumentinline.pt')
    
    ##code-section methodsinline
    implements(IViewView)
        
    ##/code-section methodsinline     

class DPDocumentdocimageView(BrowserView):
    """Additional View
    """
    
    
    ##code-section methodsdocimage
    def __call__(self):
        """
        """
        request = self.request
        alsoProvides(request, IDisableCSRFProtection)        
        refresh = request.get("refresh", False)
        response = request.RESPONSE
        response.setHeader('Content-Type', 'image/png')
        print "docimage"
        doc = self.context
        img = doc.getRepresentativeImage()
        if img:
            dateiname = '%s.%s' % (img.getId(), "png")
            header_value= contentDispositionHeader('inline', filename=dateiname, charset='latin-1')
            response.setHeader('Content-disposition', header_value)
            response.setHeader('Content-Length', len(img.image.data))
            return img.image.data
        img = doc.pdfImage()
        if img and not refresh:
            dateiname = '%s.%s' % (img.getId(), "png")
            header_value= contentDispositionHeader('inline', filename=dateiname, charset='latin-1')
            response.setHeader('Content-disposition', header_value)
            response.setHeader('Content-Length', len(img.data))
            return img.data
            
        pdf = doc.getRepresentativePDF()
        if pdf:
            execute_under_special_role(doc, "Manager", DPDocument.generatePdfImage, doc, pdf )
            img = doc.pdfImage()
            dateiname = '%s.%s' % (img.getId(), "png")
            header_value= contentDispositionHeader('inline', filename=dateiname, charset='latin-1')
            response.setHeader('Content-disposition', header_value)
            response.setHeader('Content-Length', len(img.data))
            return img.data
        # TODO: support default image in DocType
    ##/code-section methodsdocimage     


##code-section bottom
##/code-section bottom