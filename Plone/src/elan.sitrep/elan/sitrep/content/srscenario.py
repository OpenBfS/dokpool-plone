# -*- coding: utf-8 -*-
#
# File: srscenario.py
#
# Copyright (c) 2017 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the SRScenario content type. See srscenario.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from docpool.elan.config import ELAN_APP
from elan.sitrep.vocabularies import ModuleTypesVocabularyFactory
from plone.dexterity.content import Container
from plone.dexterity.interfaces import IEditFinishedEvent
from plone.supermodel import model
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import log
from zope.component import adapter
from zope.interface import implementer


class ISRScenario(model.Schema):
    """
    """


@implementer(ISRScenario)
class SRScenario(Container):
    """
    """

    security = ClassSecurityInfo()

    APP = ELAN_APP

    def getSRScenarioNames(self):
        """
        Index Method
        """
        return [self.getId()]

    def getSRScenarioRefs(self):
        """
        Index Method
        """
        return [self.UID()]

    def modTypes(self):
        """
        """
        return ModuleTypesVocabularyFactory(self, raw=True)

    def modTypeIds(self):
        mtypes = self.modTypes()
        return [mt[0] for mt in mtypes]

    def getSRScenarios(self):
        """
        """
        return [self]

    def mySRScenario(self):
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

    def getSRPhases(self, **kwargs):
        """
        """
        args = {'portal_type': 'SRPhase'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]


@adapter(ISRScenario, IEditFinishedEvent)
def updated(obj, event=None):
    log("SRScenario updated: %s" % str(obj))
    sr_cat = getToolByName(obj, "sr_catalog")
    sr_cat._reindexObject(obj)
