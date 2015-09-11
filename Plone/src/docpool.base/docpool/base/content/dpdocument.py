# -*- coding: utf-8 -*-
#
# File: dpdocument.py
#
# Copyright (c) 2015 by Condat AG
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
from collective import dexteritytextindexer
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder
from Products.CMFPlone.utils import log, log_exc

from plone.dexterity.content import Container
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
from plone import api
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zExceptions import BadRequest
##/code-section imports 

from docpool.base.config import PROJECTNAME

from docpool.base import ELAN_EMessageFactory as _

class IDPDocument(form.Schema, IDocument, IContentBase):
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


class DPDocument(Container, Document, ContentBase):
    """
    """
    security = ClassSecurityInfo()
    
    implements(IDPDocument)
    
##code-section methods




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
    
    def docTypeObj(self):
        """
        """
        et = self.dp_type()
        if not et: # The object is just being initialized and the attributes have not yet been saved
            et = self.REQUEST.get('docType','')
        #print et
        #dto = queryForObject(self, id=et)
        dto = None
        try:
            dto = self.config[et]
        except Exception, e:
            # et can be empty
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
        return mtool.getAuthenticatedMember().has_role("Owner", self)
            
    def testMethod(self):
        """
        """
        return queryForObject(self, UID="efae65b42664424e8f3eaacc744ad4b2")
    
    def change_position(self, position, id, ptype):
        """
        Move a file or an image within the document.
        """
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
