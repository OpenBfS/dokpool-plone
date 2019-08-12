# -*- coding: utf-8 -*-
#
# File: doctypes.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the DocTypes content type. See doctypes.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from plone.dexterity.content import Container
from plone.directives import form
from zope.interface import implements


class IDocTypes(form.Schema):
    """
    """


class DocTypes(Container):
    """
    """

    security = ClassSecurityInfo()

    implements(IDocTypes)

    def myDocTypes(self):
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

    def getDocTypes(self, **kwargs):
        """
        """
        args = {'portal_type': 'DocType'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getSRModuleTypes(self, **kwargs):
        """
        """
        args = {'portal_type': 'SRModuleType'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]
