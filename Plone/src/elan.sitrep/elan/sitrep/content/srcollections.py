# -*- coding: utf-8 -*-
#
# File: srcollections.py
#
# Copyright (c) 2017 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the SRCollections content type. See srcollections.py for more
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

from docpool.elan.config import ELAN_APP

from elan.sitrep.config import PROJECTNAME

from elan.sitrep import DocpoolMessageFactory as _

class ISRCollections(form.Schema):
    """
    """



class SRCollections(Container):
    """
    """
    security = ClassSecurityInfo()

    implements(ISRCollections)

    APP = ELAN_APP

    def mySRCollections(self):
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

    def getSRCollections(self, **kwargs):
        """
        """
        args = {'portal_type':'SRCollection'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getSRCollectionss(self, **kwargs):
        """
        """
        args = {'portal_type':'SRCollections'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]


