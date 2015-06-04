# -*- coding: utf-8 -*-
#
# File: groupfolder.py
#
# Copyright (c) 2015 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the GroupFolder content type. See groupfolder.py for more
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
from docpool.base.content.simplefolder import SimpleFolder, ISimpleFolder

from Products.CMFCore.utils import getToolByName

##code-section imports
##/code-section imports 

from docpool.base.config import PROJECTNAME

from docpool.base import ELAN_EMessageFactory as _

class IGroupFolder(form.Schema, ISimpleFolder):
    """
    """

##code-section interface
##/code-section interface


class GroupFolder(Container, SimpleFolder):
    """
    """
    security = ClassSecurityInfo()
    
    implements(IGroupFolder)
    
##code-section methods
    def getGroupOfFolder(self):
        """
        """
        gtool = getToolByName(self, "portal_groups")
        grp = gtool.getGroupById(self.getId())
        return grp
##/code-section methods 

    def myGroupFolder(self):
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

    def getInfoFolders(self, **kwargs):
        """
        """
        args = {'portal_type':'InfoFolder'}
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
