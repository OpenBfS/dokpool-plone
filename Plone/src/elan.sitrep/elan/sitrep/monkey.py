# -*- coding: utf-8 -*-

from docpool.base.content.documentpool import DocumentPool
from elan.sitrep.structures import createConfig
from elan.sitrep.testdata import createTestData
from elan.sitrep.testdata import deleteTestData
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides


def createSRTestData(self, prune=False):
    """
    """
    request = self.REQUEST
    alsoProvides(request, IDisableCSRFProtection)
    if prune:
        deleteTestData(self)
    createTestData(self)
    return self.restrictedTraverse("@@view")()


if not hasattr(DocumentPool, "createSRTestData"):
    DocumentPool.createSRTestData = createSRTestData


def createSRConfig(self):
    """
    """
    request = self.REQUEST
    alsoProvides(request, IDisableCSRFProtection)
    createConfig(self)
    return self.restrictedTraverse("@@view")()


if not hasattr(DocumentPool, "createSRConfig"):
    DocumentPool.createSRConfig = createSRConfig
