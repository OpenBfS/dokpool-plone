#
# File: elancurrentsituation.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ""
__docformat__ = "plaintext"

"""Definition of the ELANCurrentSituation content type. See elancurrentsituation.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from docpool.elan.config import ELAN_APP
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IELANCurrentSituation(model.Schema):
    """ """


@implementer(IELANCurrentSituation)
class ELANCurrentSituation(Container):
    """ """

    security = ClassSecurityInfo()

    APP = ELAN_APP

    def correctAllDocTypes(self):
        """ """
        # Correct references
        mpath = self.dpSearchPath()
        from docpool.base.utils import queryForObjects

        ecs = queryForObjects(self, path=mpath, portal_type="ELANDocCollection")
        for ec in ecs:
            ec.getObject().correctDocTypes()

    def myELANCurrentSituation(self):
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

    def getDashboardCollections(self, **kwargs):
        """ """
        args = {"portal_type": "DashboardCollection"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getDocuments(self, **kwargs):
        """ """
        args = {"portal_type": "Document"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getELANDocCollections(self, **kwargs):
        """ """
        args = {"portal_type": "ELANDocCollection"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getELANSections(self, **kwargs):
        """ """
        args = {"portal_type": "ELANSection"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getSRCollections(self, **kwargs):
        """ """
        args = {"portal_type": "SRCollection"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]
