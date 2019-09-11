# -*- coding: utf-8 -*-
#
# File: srmoduletypes.py
#
# Copyright (c) 2017 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the SRModuleTypes content type. See srmoduletypes.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from docpool.elan.config import ELAN_APP
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class ISRModuleTypes(model.Schema):
    """
    """


@implementer(ISRModuleTypes)
class SRModuleTypes(Container):
    """
    """

    security = ClassSecurityInfo()

    APP = ELAN_APP

    def mySRModuleTypes(self):
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

    def getSRModuleTypes(self, **kwargs):
        """
        """
        args = {'portal_type': 'SRModuleType'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]
