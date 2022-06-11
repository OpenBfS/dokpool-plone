#
# File: srconfig.py
#
# Copyright (c) 2017 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ""
__docformat__ = "plaintext"

"""Definition of the SRConfig content type. See srconfig.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from docpool.elan.config import ELAN_APP
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class ISRConfig(model.Schema):
    """ """


@implementer(ISRConfig)
class SRConfig(Container):
    """ """

    security = ClassSecurityInfo()

    APP = ELAN_APP

    def mySRConfig(self):
        """ """
        return self

    def getFirstChild(self):
        """ """
        fc = self.getFolderContents()
        if len(fc) > 0:
            return fc[0].getObject()
        else:
            return None

    def getAllContentObjects(self):
        """ """
        return [obj.getObject() for obj in self.getFolderContents()]

    def getSRCollectionss(self, **kwargs):
        """ """
        args = {"portal_type": "SRCollections"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getSRScenarios(self, **kwargs):
        """ """
        args = {"portal_type": "SRScenario"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getSRTextBlockss(self, **kwargs):
        """ """
        args = {"portal_type": "SRTextBlocks"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]
