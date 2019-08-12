# -*- coding: utf-8 -*-
#
# File: dpapplication.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the DPApplication content type. See dpapplication.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from plone.dexterity.content import Container
from plone.directives import form
from zope.interface import implements


class IDPApplication(form.Schema):
    """
    """


class DPApplication(Container):
    """
    """

    security = ClassSecurityInfo()

    implements(IDPApplication)

    def myDPApplication(self):
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
        args = {'portal_type': 'File'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getImages(self, **kwargs):
        """
        """
        args = {'portal_type': 'Image'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]
