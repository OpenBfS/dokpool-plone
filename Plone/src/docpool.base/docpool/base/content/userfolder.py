# -*- coding: utf-8 -*-
#
# File: userfolder.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the UserFolder content type. See userfolder.py for more
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
from docpool.base.content.simplefolder import SimpleFolder, ISimpleFolder

from Products.CMFCore.utils import getToolByName

##code-section imports
from docpool.base.utils import execute_under_special_role, _cutPaste
##/code-section imports 

from docpool.base.config import PROJECTNAME

from docpool.base import DocpoolMessageFactory as _

class IUserFolder(form.Schema, ISimpleFolder):
    """
    """

##code-section interface
##/code-section interface


class UserFolder(Container, SimpleFolder):
    """
    """
    security = ClassSecurityInfo()
    
    implements(IUserFolder)
    
##code-section methods
    def notifyMemberAreaCreated(self):
        """
        Move the member area to the proper location.
        """
        # print "notifyMemberAreaCreated"
        def moveFolder():
            # Determine the owner
            o = self.getOwner()
            if o:
                # Determine the corresponding ESD
                esd_uid = o.getProperty("dp")
                if esd_uid:
                    catalog = getToolByName(self, 'portal_catalog')
                    result  = catalog({'UID' : esd_uid})
                    if len(result) == 1:
                        esd = result[0].getObject()
                # Move me there
                        members = esd.content.Members
                        _cutPaste(self, members, unique=True)
        execute_under_special_role(self, "Manager", moveFolder)
##/code-section methods 

    def myUserFolder(self):
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
