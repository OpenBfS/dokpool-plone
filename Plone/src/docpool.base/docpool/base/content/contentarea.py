# -*- coding: utf-8 -*-
#
# File: contentarea.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the ContentArea content type. See contentarea.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from plone.dexterity.content import Container
from plone.directives import form
from zope.interface import implements


class IContentArea(form.Schema):
    """
    """


class ContentArea(Container):
    """
    """

    security = ClassSecurityInfo()

    implements(IContentArea)

    def myContentArea(self):
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

    def getGroupss(self, **kwargs):
        """
        """
        args = {'portal_type': 'Groups'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getUserss(self, **kwargs):
        """
        """
        args = {'portal_type': 'Users'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]
