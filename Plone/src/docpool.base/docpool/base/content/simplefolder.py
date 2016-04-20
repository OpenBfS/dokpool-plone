# -*- coding: utf-8 -*-
#
# File: simplefolder.py
#
# Copyright (c) 2016 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the SimpleFolder content type. See simplefolder.py for more
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
from docpool.base.content.folderbase import FolderBase, IFolderBase

from Products.CMFCore.utils import getToolByName

##code-section imports
from elan.esd.utils import getScenariosForCurrentUser
from docpool.base.utils import queryForObjects, portalMessage, execute_under_special_role, \
getAllowedDocumentTypes
from Products.CMFPlone.utils import parent
from zope.interface import alsoProvides
from plone.protect.interfaces import IDisableCSRFProtection
##/code-section imports 

from docpool.base.config import PROJECTNAME

from docpool.base import ELAN_EMessageFactory as _

class ISimpleFolder(form.Schema, IFolderBase):
    """
    """
        
    allowedDocTypes = schema.List(
                        title=_(u'label_simplefolder_alloweddoctypes', default=u'Document types allowed in this folder'),
                        description=_(u'description_simplefolder_alloweddoctypes', default=u'Leave blank to enable all types configured for the group.'),
                        required=False,
##code-section field_allowedDocTypes
                        value_type=schema.Choice(source="docpool.base.vocabularies.GroupDocType"),
##/code-section field_allowedDocTypes                           
    )
    

##code-section interface
##/code-section interface


class SimpleFolder(Container, FolderBase):
    """
    """
    security = ClassSecurityInfo()
    
    implements(ISimpleFolder)
    
##code-section methods
    def customMenu(self, menu_items):
        """
        """
        dts = getAllowedDocumentTypes(self)
        filter = False
        if self.allowedDocTypes:
            filter = True
        res = []
        for menu_item in menu_items:
            if menu_item.get('id') == 'DPDocument':
                for dt in dts:
                    if not dt.getObject().globalAllow: # only generally allowed doctypes
                        continue
                    if not filter or dt.id in self.allowedDocTypes:
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

    def getUserSelectedScenarios(self):
        """
        """
        usc = getScenariosForCurrentUser(self)
        return usc

    def isPrincipalFolder(self):
        """
        """
        return self.getPortalTypeName() in ['UserFolder', 'GroupFolder']

    def canBeDeleted(self, principal_deleted=False):
        """
        A folder can be deleted, if
        - it does not contain published Documents somewhere below AND
        - it is not a member or group root folder, 
              unless principal_deleted = True 
        """
        mtool = getToolByName(self, "portal_membership")
        if not mtool.checkPermission("Delete objects", self):
            return False       
        if self.containsPublishedDocuments():
            return False
        if self.isPrincipalFolder():
            if principal_deleted:
                return True
            else:
                return False
        return True
    
    def containsPublishedDocuments(self):
        """
        """
        return len(queryForObjects(self, path="/".join(self.getPhysicalPath()), portal_type="DPDocument", review_state="published")) > 0
    
    
    def publish_doc(self, id, REQUEST=None):
        """
        """
        if REQUEST:
            alsoProvides(REQUEST, IDisableCSRFProtection)        
        doc = None
        try:
            doc = self._getOb(id)
        except:
            pass
        if doc:
            wftool = getToolByName(self, 'portal_workflow')
            wftool.doActionFor(doc, 'publish')
            if REQUEST:
                portalMessage(self, _("The document has been published."), "info")
                return self.restrictedTraverse("@@view")()
            
        
        
##/code-section methods 

    def mySimpleFolder(self):
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

    def getSimpleFolders(self, **kwargs):
        """
        """
        args = {'portal_type':'SimpleFolder'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 


##code-section bottom
##/code-section bottom 
