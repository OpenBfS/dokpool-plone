# -*- coding: utf-8 -*-

from docpool.base.content.documentpool import DocumentPool
from elan.sitrep.testdata import deleteTestData, createTestData
from zope.interface import alsoProvides
from plone.protect.interfaces import IDisableCSRFProtection


def createSRTestData(self, prune=False):
    """
    """
    request = self.REQUEST
    alsoProvides(request, IDisableCSRFProtection)        
    if prune:
        deleteTestData(self)
    createTestData(self)

if not hasattr(DocumentPool, "createSRTestData"):
    DocumentPool.createSRTestData = createSRTestData
    
