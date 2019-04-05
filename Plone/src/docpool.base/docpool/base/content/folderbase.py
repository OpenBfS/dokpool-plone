# -*- coding: utf-8 -*-
#
# File: folderbase.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the FolderBase content type. See folderbase.py for more
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
from docpool.base.content.contentbase import ContentBase, IContentBase

from Products.CMFCore.utils import getToolByName

##code-section imports
from zope.interface import alsoProvides
from plone.protect.interfaces import IDisableCSRFProtection
from docpool.base.utils import portalMessage
##/code-section imports 

from docpool.base.config import PROJECTNAME

from docpool.base import DocpoolMessageFactory as _

class IFolderBase(form.Schema, IContentBase):
    """
    """

##code-section interface
##/code-section interface


class FolderBase(Container, ContentBase):
    """
    """
    security = ClassSecurityInfo()
    
    implements(IFolderBase)
    
##code-section methods
    def change_state(self, id, action, backToReferer=False, REQUEST=None):
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
                if str(action) == 'publish': # when publishing we also publish any document inside the current document
                    for subdoc in doc.getDPDocuments():
                        try:
                            wftool.doActionFor(subdoc, action)
                        except:
                            pass
            except:
                return self.restrictedTraverse("@@view")()
            if REQUEST:
                last_referer = REQUEST.get('HTTP_REFERER')
                portalMessage(self, _("The document state has been changed."), "info")
                if backToReferer and last_referer:
                    return REQUEST.RESPONSE.redirect(last_referer)
                else:
                    return self.restrictedTraverse("@@view")()

    def canBeDeleted(self, principal_deleted=False):
        """
        """
        mtool = getToolByName(self, "portal_membership")
        if not mtool.checkPermission("Delete objects", self):
            return False       
        else:
            return True
##/code-section methods 

    def myFolderBase(self):
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
##/code-section bottom 
