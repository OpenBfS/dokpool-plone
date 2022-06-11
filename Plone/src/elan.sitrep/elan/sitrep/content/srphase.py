#
# File: srphase.py
#
# Copyright (c) 2017 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ""
__docformat__ = "plaintext"

"""Definition of the SRPhase content type. See srphase.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from plone.dexterity.content import Container
from plone.dexterity.interfaces import IEditFinishedEvent
from plone.supermodel import model
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import log
from zope.component import adapter
from zope.interface import implementer


class ISRPhase(model.Schema):
    """ """


@implementer(ISRPhase)
class SRPhase(Container):
    """ """

    security = ClassSecurityInfo()

    def getSRPhaseNames(self):
        """
        Index method
        """
        return [self.getId()]

    def getSRPhaseRefs(self):
        """
        Index method
        """
        return [self.UID()]

    def getPhaseTitle(self):
        """ """
        return "{}: {}".format(
            self.mySRScenario().Title(),
            self.Title(),
        )

    def availableModuleConfigs(self):
        mtypes = self.modTypes()
        res = {}
        for mt in mtypes:
            res[mt[0]] = None
        mcs = self.getSRModuleConfigs()
        for mc in mcs:
            res[mc.modType] = mc
        return res

    def mySRPhase(self):
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

    def getSRModuleConfigs(self, **kwargs):
        """ """
        args = {"portal_type": "SRModuleConfig"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]


@adapter(ISRPhase, IEditFinishedEvent)
def updated(obj, event=None):
    log("SRPhase updated: %s" % str(obj))
    sr_cat = getToolByName(obj, "sr_catalog")
    sr_cat._reindexObject(obj)
