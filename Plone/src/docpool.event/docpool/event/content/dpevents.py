#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ""
__docformat__ = "plaintext"

from AccessControl import ClassSecurityInfo
from logging import getLogger
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
