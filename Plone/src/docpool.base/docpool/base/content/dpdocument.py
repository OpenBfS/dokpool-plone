# -*- coding: utf-8 -*-
#
# File: dpdocument.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the DPDocument content type. See dpdocument.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from zope.interface import implements
from zope.component import adapts
from zope import schema
from plone.directives import form, dexterity
from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage
from collective import dexteritytextindexer
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder
from Products.CMFPlone.utils import log, log_exc

from plone.dexterity.content import Container
from docpool.base.content.extendable import Extendable, IExtendable
from docpool.base.content.contentbase import ContentBase, IContentBase
from plone.app.contenttypes.content import Document,IDocument

from Products.CMFCore.utils import getToolByName

##code-section imports
from docpool.base.utils import queryForObject, queryForObjects, execute_under_special_role,\
    _copyPaste, getUserInfo, portalMessage
from Products.CMFPlone.utils import log, log_exc
from plone.app.discussion.interfaces import IConversation
from Products.Archetypes.utils import DisplayList, shasattr
from zope.container.interfaces import IContainerModifiedEvent, IObjectRemovedEvent
from zope.component import adapter
from plone import api, namedfile
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zExceptions import BadRequest
from plone.memoize import ram
import re
from docpool.base.pdfconversion import get_images, metadata, pdfobj, data
from zope.annotation.interfaces import IAnnotations
from BTrees.OOBTree import OOBTree
from StringIO import StringIO
from docpool.base import DocpoolMessageFactory as _
from Acquisition import aq_base, aq_parent
from plone.dexterity.utils import safe_unicode
from plone.api import content
from PIL import Image
from zope.interface import alsoProvides
from plone.protect.interfaces import IDisableCSRFProtection
from zope.component import getMultiAdapter
##/code-section imports

from docpool.base.config import PROJECTNAME

from docpool.base import DocpoolMessageFactory as _

class IDPDocument(form.Schema, IDocument, IExtendable, IContentBase):
    """
    """
        
    docType = schema.Choice(
                        title=_(u'label_dpdocument_doctype', default=u'Document Type'),
                        description=_(u'description_dpdocument_doctype', default=u''),
                        required=True,
##code-section field_docType
                        source="docpool.base.vocabularies.DocumentTypes",
##/code-section field_docType                           
    )
    
    dexteritytextindexer.searchable('text')    
    text = RichText(
                        title=_(u'label_dpdocument_text', default=u'Text'),
                        description=_(u'description_dpdocument_text', default=u''),
                        required=True,
##code-section field_text
##/code-section field_text                           
    )
    

##code-section interface
##/code-section interface


class DPDocument(Container, Document, Extendable, ContentBase):
    """
    """
    security = ClassSecurityInfo()
    
    implements(IDPDocument)
    
##code-section methods
    def change_state(self, id, action, REQUEST=None):
        """
        """
        if REQUEST:
            alsoProvides(REQUEST, IDisableCSRFProtection)
        if not action:
            return self.restrictedTraverse("@@view")()
        doc = None
        try:
            doc = self._getOb(id)
        except:
            pass
        if doc:
            wftool = getToolByName(self, 'portal_workflow')
            try:
                wftool.doActionFor(doc, action)
                if str(action) == 'publish':  # when publishing we also publish any document inside the current document
                    for subdoc in doc.getDPDocuments():
                        try:
                            wftool.doActionFor(subdoc, action)
                        except:
                            pass
            except:
                return self.restrictedTraverse("@@view")()
            if REQUEST:
                portalMessage(self, _("The document state has been changed."), "info")
                return self.restrictedTraverse("@@view")()

    def isClean(self):
        """
        Is this document free for further action like publishing or transfer.
        @return:
        """
        request = self.REQUEST
        dp_app_state = getMultiAdapter((self, request), name=u'dp_app_state')
        def _isClean():
            lbs = dp_app_state.appsEffectiveForObject(request)
            for lb in lbs:
                if not self.doc_extension(lb).isClean():
                    return False
            return self.unknownDocType() is None
        # We need to do this as Manager, because we need to check for all possible
        # reasons why a document could not by worked upon. Not just the reasons we
        # would be allowed to see as a user.
        return execute_under_special_role(self, "Manager", _isClean)

    def createActions(self):
        """
        We need to check if special workflows are needed depending on the user's role.
        """
        f = self.myFolderBase()
        r = api.user.get_roles(obj=f, inherit=True)
        if "Owner" in r:
            return
        if "Reviewer" in r:
            log("Setting Guest Workflow on Document " + self.getId())
    
            placeful_wf = getToolByName(self, 'portal_placeful_workflow')
            try:
                self.manage_addProduct['CMFPlacefulWorkflow'].manage_addWorkflowPolicyConfig()
            except BadRequest, e:
                log_exc(e)
            config = placeful_wf.getWorkflowPolicyConfig(self)
            placefulWfName = 'dp-guest-document'
            config.setPolicyIn(policy=placefulWfName, update_security=False)
            config.setPolicyBelow(policy=placefulWfName, update_security=False)
            self.reindexObject()
            self.reindexObjectSecurity()
            
    def getAllowedSubTypes(self):
        dto = self.docTypeObj()
        if dto:
            adt = dto.allowedDocTypes
            if adt:
                return [ dt.to_object for dt in adt ]
        return []

    def customMenu(self, menu_items):
        """
        """
        res1 = []
        if not self.uploadsAllowed():
            for menu_item in menu_items:
                if (menu_item.get('id') in ['File', 'Image']):
                    continue
                res1.append(menu_item)
        else:
            res1 = menu_items
        dts = self.getAllowedSubTypes()
        res = []
        for menu_item in res1:
            if menu_item.get('id') == 'DPDocument':
                for dt in dts:
                    res.append({'extra': 
                               {'separator': None, 'id': dt.id, 'class': 'contenttype-%s' % dt.id}, 
                                'submenu': None, 
                                'description': '', 
                                'title': dt.Title, 
                                'action': '%s/++add++DPDocument?form.widgets.docType:list=%s' % (self.absolute_url(), dt.id), 
                                'selected': False, 
                                'id': dt.id, 
                                'icon': None})
            else:
                res.append(menu_item)
        return res


    def allSubobjectsPublished(self):
        """

        @return:
        """
        for obj in self.getDPDocuments():
            if api.content.get_state(obj) != 'published':
                return False
        return True

    def workflowActions(self):
        """
        """
        wf_tool = getToolByName(self, 'portal_workflow')
        workflowActions = wf_tool.listActionInfos(object=self)
        results = []
        for action in workflowActions:
            if action['category'] != 'workflow':
                continue

            description = ''

            transition = action.get('transition', None)
            if transition is not None:
                description = transition.description

            if action['allowed']:
                results.append({
                    'id': action['id'],
                    'title': action['title'],
                    'description': description,
                    'icon': action['id'] + ".png",
                })        
        return results        
        
    def unknownDocType(self):
        """
        If my doc type is in state private, return it.
        """
        dt = self.docTypeObj()
        if dt:
            tstate = api.content.get_state(dt)
            if tstate == 'private':
                return dt
        return None        
     
    def changed(self):
        """
        """
        return self.getMdate() 

        
    def vocabDocType(self):
        """
        """
        cat = getToolByName(self, "portal_catalog")
        types = cat({"portal_type":"DocType", "sort_on": "sortable_title", "path": self.dpSearchPath()})
        return [ (brain.id, brain.Title) for brain in types ]
    
    def dp_type(self):
        """
        """
        return self.docType
    
    def _docTypeObj_cachekey(method, self):
        return (self.absolute_url_path(), self.modified)
    
    #@ram.cache(_docTypeObj_cachekey)
    def docTypeObj(self):
        """
        """
        et = self.dp_type()
        if not et: # The object is just being initialized and the attributes have not yet been saved
            et = self.REQUEST.get('docType','')
        #dto = queryForObject(self, id=et)
        dto = None
        try:
            dto = self.config.dtypes[et]
        except Exception, e:
            # et can be empty
            # print e
            pass
        if not dto:
            log("No DocType Object for type name '%s'" % self.dp_type())
        return dto
        
        
    def dp_type_name(self):
        """
        """
        dto = self.docTypeObj()
        if dto:
            return dto.title
        else:
            return ""
            
    def publishedImmediately(self, raw=False):
        """
        """
        dto = self.docTypeObj()
        if dto: 
            if not raw:
                # We only publish immediately when uploads are not allowed
                # and if we are not in a personal folder
                # print dto.publishImmediately, dto.allowUploads, self.isIndividual()
                return dto.publishImmediately and not dto.allowUploads and not self.isIndividual()
            else:
                return dto.publishImmediately
        else:
            return False
        
    def uploadsAllowed(self):
        """
        """
        mtool = getToolByName(self, "portal_membership")
        if not mtool.checkPermission("Add portal content", self):
            return False      
        dto = self.docTypeObj()
        if dto:
            return dto.allowUploads
        else:
            return False        
        
    def canBeDeleted(self):
        """
        """
        mtool = getToolByName(self, "portal_membership")
        return mtool.checkPermission("Delete objects", self)

    def canBeEdited(self):
        """
        """
        mtool = getToolByName(self, "portal_membership")
        return mtool.checkPermission("Modify portal content", self)
    
    def isInOneOfMyFolders(self):
        """
        Determine if the document is either in the users personal folder or in one of his groups.
        This should be defined by the Owner role on the object.
        """
        mtool = getToolByName(self, "portal_membership")
        return (mtool.getAuthenticatedMember().has_role("Owner", self) or mtool.getAuthenticatedMember().has_role("Reviewer", self))
            
    def testMethod(self):
        """
        """
        return queryForObject(self, UID="efae65b42664424e8f3eaacc744ad4b2")
    
    def change_position(self, position, id, ptype):
        """
        Move a file or an image within the document.
        """
        request = self.REQUEST
        alsoProvides(request, IDisableCSRFProtection)                
        position=position.lower()
        # we need to find all other ids for the same type
        ssids = [o.getId for o in self.getFolderContents({'portal_type':ptype})]
        #print ssids
        if   position=='up':
            self.moveObjectsUp(id, 1, ssids)
        elif position=='down':
            self.moveObjectsDown(id, 1, ssids)
        self.plone_utils.reindexOnReorder(self)        
        return self.restrictedTraverse("@@view")()

    def hasComments(self):
        """
        """
        conversation = IConversation(self)
        return len(conversation.objectIds()) > 0
            
    def Identifier(self):
        """
        We offer this method here on the object, so that it is used by the RSS template.
        """
        dto = self.docTypeObj()
        if dto:
            cat = dto.contentCategory
            if cat:
                return "%s/@@dview?d=%s&disable_border=1" % (cat.absolute_url(), self.UID())
        return self.absolute_url()
    
    def SearchableText(self):
        """
        We override, so we get the content of all subobjects indexed.
        """
        st = Document.SearchableText(self) #TODO? searchable
        stsub = [ obj.SearchableText() for obj in self.getAllContentObjects()]
        return st + " " + " ".join(stsub)
    
    def getRepresentativeImage(self):
        """
        """
        imgPattern = self.docTypeObj().imgPattern
        if imgPattern:
            p = re.compile(imgPattern, re.IGNORECASE)
            images = self.getImages()
            for image in images:
                if p.match(image.getId()):
                    return image
        else:
            return None
        
    def getRepresentativePDF(self):
        """
        """
        pdfPattern = self.docTypeObj().pdfPattern
        if pdfPattern:
            p = re.compile(pdfPattern, re.IGNORECASE)
            files = self.getFiles()
            for f in files:
                if p.match(f.getId()):
                    return f
        else:
            return None
        
    def generatePdfImage(self, pdffile):
        """
        """
        pdf = pdfobj(pdffile)
        # Use BTrees
        storage = OOBTree()
        img = get_images(pdffile, 0, 1)
        storage['image_thumbnails'] = img
        meta = metadata(pdf)
        storage['metadata'] = meta

        annotations = IAnnotations(self)
        annotations['pdfimages'] = storage

        self.reindexObject()
        
        
    def pdfImage(self):
        """
        """
        annotations = IAnnotations(self)
        if 'pdfimages' in annotations:
            image = annotations['pdfimages']['image_thumbnails']["1_preview"]
            return image
        else:
            return None
        
    def autocreateSubdocuments(self):
        """
        TODO: specifically for XMLRPC usage
        """
        # * Von den allowed Types alle autocreatable Types durchgehen und ihre Muster "ausprobieren"
        # * Wenn Files oder Images gefunden zu einem Muster: entsprechendes DPDocument erzeugen und Files/Images verschieben
        return "ok"
        
    def setDPProperty(self, name, value, ptype="string"):
        """
        """
        alsoProvides(self.REQUEST, IDisableCSRFProtection)
        if not self.hasProperty(name):
            self.manage_addProperty(name, value, ptype)
        else:
            self._updateProperty(name, value)
        return "set"

    def deleteDPProperty(self, name):
        """
        """
        alsoProvides(self.REQUEST, IDisableCSRFProtection)
        if self.hasProperty(name):
            self._delProperty(name)
            return "deleted"
        return "unknown"

    def getDPProperty(self, name):
        """
        """
        if self.hasProperty(name):
            return self.getProperty(name)

    def getDPProperties(self):
        """
        """
        return self.propertyItems()
        
    def readPropertiesFromFile(self):
        """
        """
        files = self.getFiles()
        msg = "none"
        for f in files:
            if f.getId() == "properties.txt":
                d = StringIO(data(f))
                props = d.readlines()
                for prop in props:
                    if prop and len(prop) > 2:
                        name, value = prop.split("=")
                        name = name.strip()
                        value = value.strip()
                        ptype = "string"
                        try:
                            name, ptype = name.split(":")
                        except:
                            pass
                        self.setDPProperty(name, value, ptype)
                        msg = "set"
        return msg

    def getFileOrImageByPattern(self, pattern):
        """
        """
#        print pattern
#        print self.getAllContentObjects()
        p = re.compile(pattern, re.IGNORECASE)
        for obj in self.getAllContentObjects():
#            print obj.getId()
            if p.match(obj.getId()):
#                print obj
                return obj
    
    def getMapImageObj(self):
        """
        The map image is expected to be a file with with a name like 'xxx-map.png' or 'yyy_map.jpg'.
        """
        return self.getFileOrImageByPattern(".*[-_]map\..*")
            
    def getMapImage(self, scale=""):
        """
        """
        img = self.getMapImageObj()
        if img:
            return "<img src='%s%s' />" % (img.absolute_url(), scale)
        else:
            return _(u"No map image")

    def getLegendImageObj(self):
        """
        """
        return self.getFileOrImageByPattern(".*[-_]legend\..*")
    
    def getLegendImage(self, scale=""):
        """
        """
        img = self.getLegendImageObj()
        if img:
            return "<img src='%s%s' />" % (img.absolute_url(), scale)
        else:
            return _(u"No legend image")

    def getMyImage(self, refresh=False, full=True):
        """
        1. the map image, otherwise
        2. the representative image, otherwise
        3. try to generate an image from PDF
        4. Take the first image available in the doc
        5. a default image
        @param refresh: True --> generate afresh from PDF if necessary
        @param full: True --> combine map & legend images
        @return: a tuple with an image and a filename
        """
        alsoProvides(self.REQUEST, IDisableCSRFProtection)

        doc = self
        mapimg = self.getMapImageObj()
        if mapimg:
            legendimg = self.getLegendImageObj()
            dateiname = '%s.%s' % (mapimg.getId(), "png")
            if not full or not legendimg:
                return mapimg.image.data, dateiname
            else:
                #combine into one image if full=True and legend available
                images = map(Image.open, [StringIO(mapimg.image.data), StringIO(legendimg.image.data)])
                w = sum(i.size[0] for i in images)
                mh = max(i.size[1] for i in images)
                
                result = Image.new("RGBA", (w, mh), "white")
                
                x = 0
                for i in images:
                    result.paste(i, (x, 0))
                    x += i.size[0]
                res = StringIO()
                result.save(res, 'PNG')
                return res.getvalue(), dateiname

                      
        img = doc.getRepresentativeImage()
        if img:
            dateiname = '%s.%s' % (img.getId(), "png")
            return img.image.data, dateiname
        img = doc.pdfImage()
        if img and not refresh:
            dateiname = '%s.%s' % (img.getId(), "png")
            return img.data.data, dateiname
            
        pdf = doc.getRepresentativePDF()
        if pdf:
            execute_under_special_role(doc, "Manager", DPDocument.generatePdfImage, doc, pdf )
            img = doc.pdfImage()
            dateiname = '%s.%s' % (img.getId(), "png")
            return img.data, dateiname


        img = doc.getFirstImageObj()
        if img:
            dateiname = '%s.%s' % (img.getId(), "png")
            return img.image.data, dateiname
        # TODO: Idea: support default image in DocType
        # Show Default image, if no other image is available
        img = getattr(self,'docdefaultimage.png')
        return img._data, 'docdefaultimage.png'
        

    def image(self):
        """
        """
        # We need to acquire Manager rights here, since we are called in traversal code,
        # which unfortunately comes as Anoymous
        data, filename = execute_under_special_role(self, "Manager", self.getMyImage, False)
        return namedfile.NamedImage(data, filename=safe_unicode(filename))

    def myState(self):
        """
        """
        return content.get_state(self, "None")
    
    def getFirstImage(self, scale=""):
        img = self.getFirstImageObj()
        if img:
            return "<img src='%s%s' />" % (img.absolute_url(), scale)
        else:
            return None

    def getFirstImageObj(self):
        """
        
        @return: 
        """
        imgs = self.getImages()
        if imgs:
            img = imgs[0]
            return img
        else:
            return None

##/code-section methods 

    def myDPDocument(self):
        """
        """
        return self

    def getFirstChild(self):
        """
        """
        fc = self.getFolderContents()
        if len(fc) > 0:
            return fc[0].getObject()
        else:
            return None

    def getAllContentObjects(self):
        """
        """
        return [obj.getObject() for obj in self.getFolderContents()]

    def getDPDocuments(self, **kwargs):
        """
        """
        args = {'portal_type':'DPDocument'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 

    def getFiles(self, **kwargs):
        """
        """
        args = {'portal_type':'File'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 

    def getImages(self, **kwargs):
        """
        """
        args = {'portal_type':'Image'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 


##code-section bottom
@adapter(IDPDocument, IContainerModifiedEvent)
def updateContainerModified(obj, event=None):
    """
    """
    if not obj.isArchive():
        obj.update_modified()
        obj.reindexObject() # New fulltext maybe needed


##/code-section bottom 
