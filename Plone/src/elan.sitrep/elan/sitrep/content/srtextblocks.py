# -*- coding: utf-8 -*-
#
# File: srtextblocks.py
#
# Copyright (c) 2017 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the SRTextBlocks content type. See srtextblocks.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from docpool.elan.config import ELAN_APP
from plone.dexterity.content import Container
from plone.directives import form
from zope.interface import implements


class ISRTextBlocks(form.Schema):
    """
    """


class SRTextBlocks(Container):
    """
    """

    security = ClassSecurityInfo()

    implements(ISRTextBlocks)

    APP = ELAN_APP

    def mySRTextBlocks(self):
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

    def getSRTextBlocks(self, **kwargs):
        """
        """
        args = {'portal_type': 'SRTextBlock'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getSRTextBlockss(self, **kwargs):
        """
        """
        args = {'portal_type': 'SRTextBlocks'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]
