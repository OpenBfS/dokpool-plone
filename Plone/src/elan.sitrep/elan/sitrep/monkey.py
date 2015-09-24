# -*- coding: utf-8 -*-

from docpool.base.content.documentpool import DocumentPool
from elan.sitrep.testdata import deleteTestData, createTestData


def createSRTestData(self, prune=False):
    """
    """
    if prune:
        deleteTestData(self)
    createTestData(self)

if not hasattr(DocumentPool, "createSRTestData"):
    DocumentPool.createSRTestData = createSRTestData
    
