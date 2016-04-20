# -*- coding: utf-8 -*-
#
# File: infofolder.py
#
# Copyright (c) 2016 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the InfoFolder content type. See infofolder.py for more
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
from zExceptions import BadRequest
from Products.Archetypes.utils import shasattr
##/code-section imports 

from docpool.base.config import PROJECTNAME

from docpool.base import ELAN_EMessageFactory as _

class IInfoFolder(form.Schema, IFolderBase):
    """
    """

##code-section interface
##/code-section interface


class InfoFolder(Container, FolderBase):
    """
    """
    security = ClassSecurityInfo()
    
    implements(IInfoFolder)
    
##code-section methods
    def createActions(self):
        """
        """
        if shasattr(self, "myGroupFolder", acquire=True):
            log("Creating Private Info Folder")
    
            placeful_wf = getToolByName(self, 'portal_placeful_workflow')
            try:
                self.manage_addProduct['CMFPlacefulWorkflow'].manage_addWorkflowPolicyConfig()
            except BadRequest, e:
                log_exc(e)
            config = placeful_wf.getWorkflowPolicyConfig(self)
            placefulWfName = 'dp-private-infofolder'
            config.setPolicyIn(policy=placefulWfName, update_security=False)
            config.setPolicyBelow(policy=placefulWfName, update_security=False)
            self.reindexObject()
            self.updateSecurity()
            self.reindexObjectSecurity()
##/code-section methods 

    def myInfoFolder(self):
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

    def getInfoDocuments(self, **kwargs):
        """
        """
        args = {'portal_type':'InfoDocument'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 

    def getInfoFolders(self, **kwargs):
        """
        """
        args = {'portal_type':'InfoFolder'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 

    def getInfoLinks(self, **kwargs):
        """
        """
        args = {'portal_type':'InfoLink'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 


##code-section bottom
##/code-section bottom 
