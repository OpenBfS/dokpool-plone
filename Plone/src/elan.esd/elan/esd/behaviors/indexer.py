# -*- coding: utf-8 -*-
from plone.indexer import indexer
from Products.CMFPlone import log
from docpool.base.content.dpdocument import IDPDocument
from elan.esd.behaviors.elandocument import IELANDocument

@indexer(IDPDocument)
def scenarios_indexer(obj):
    try:
        return IELANDocument(obj).scenarioIndex()
    except:
        pass

@indexer(IDPDocument)
def category_indexer(obj):
    try:
        return IELANDocument(obj).category()
    except:
        pass

@indexer(IDPDocument)
def cat_path_indexer(obj):
    try:
        return IELANDocument(obj).cat_path()
    except:
        pass