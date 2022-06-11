#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ""
__docformat__ = "plaintext"

from logging import getLogger

from AccessControl import ClassSecurityInfo
from plone.dexterity.content import Container
from plone.supermodel import model
from Products.CMFPlone.utils import parent
from zope.interface import implementer

logger = getLogger("dpevents")


class IDPEvents(model.Schema):
    """ """


@implementer(IDPEvents)
class DPEvents(Container):
    """ """

    security = ClassSecurityInfo()

    def migrate(self):
        f = parent(self)
        if hasattr(self, "_setPortalTypeName"):
            self._setPortalTypeName("DPEvents")
        myid = self.getId()
        del f[myid]
        self.__class__ = DPEvents
        f[myid] = self
        logger.info(self.__class__)
        logger.info(self.getPortalTypeName())

    def myDPEvents(self):
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

    def getDPEvents(self, **kwargs):
        """ """
        args = {"portal_type": "DPEvent"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]


class ELANScenarios(DPEvents):
    pass
