# -*- coding: utf-8 -*-
#
# File: groups.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the Groups content type. See groups.py for more
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

from Products.CMFCore.utils import getToolByName


from docpool.base.config import PROJECTNAME

from docpool.base import DocpoolMessageFactory as _


class IGroups(form.Schema):
    """
    """


class Groups(Container):
    """
    """

    security = ClassSecurityInfo()

    implements(IGroups)

    def myGroups(self):
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

    def getGroupFolders(self, **kwargs):
        """
        """
        args = {'portal_type': 'GroupFolder'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]
