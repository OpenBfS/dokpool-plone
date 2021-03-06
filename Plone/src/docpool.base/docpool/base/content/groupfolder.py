# -*- coding: utf-8 -*-
#
# File: groupfolder.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the GroupFolder content type. See groupfolder.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from docpool.base.content.simplefolder import ISimpleFolder
from docpool.base.content.simplefolder import SimpleFolder
from docpool.base.utils import RARELY_USED_TYPES
from plone.app.content.browser import constraintypes
from plone.dexterity.content import Container
from plone.supermodel import model
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import ISelectableConstrainTypes
from zope.interface import implementer


class IGroupFolder(model.Schema, ISimpleFolder):
    """
    """


@implementer(IGroupFolder)
class GroupFolder(Container, SimpleFolder):
    """
    """

    security = ClassSecurityInfo()

    def getGroupOfFolder(self):
        """
        """
        gtool = getToolByName(self, "portal_groups")
        grp = gtool.getGroupById(self.getId())
        return grp

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

    def getCollaborationFolders(self, **kwargs):
        """
        """
        args = {'portal_type': 'CollaborationFolder'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getDPDocuments(self, **kwargs):
        """
        """
        args = {'portal_type': 'DPDocument'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getInfoFolders(self, **kwargs):
        """
        """
        args = {'portal_type': 'InfoFolder'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getPrivateFolders(self, **kwargs):
        """
        """
        args = {'portal_type': 'PrivateFolder'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getReviewFolders(self, **kwargs):
        """
        """
        args = {'portal_type': 'ReviewFolder'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getSimpleFolders(self, **kwargs):
        """
        """
        args = {'portal_type': 'SimpleFolder'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def update_immediately_addable_types(self):
        constrain = ISelectableConstrainTypes(self)
        constrain.setConstrainTypesMode(constraintypes.ENABLED)
        constrain.setLocallyAllowedTypes((
            'DPDocument',
            'SimpleFolder',
            'PrivateFolder',
            'ReviewFolder',
            'CollaborationFolder',
            'InfoFolder',
            'Collection',
        ))
        # retain order of allowed types just like the stock form does
        constrain.setImmediatelyAddableTypes(('DPDocument', 'SimpleFolder'))
