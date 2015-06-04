# -*- coding: utf-8 -*-
from plone.indexer import indexer
from Products.CMFPlone import log
from docpool.base.content.dpdocument import IDPDocument
from elan.esd.behaviors.elandocument import IELANDocument

@indexer(IDPDocument)
def scenarios_indexer(obj):
    return IELANDocument(obj).scenarioIndex()

@indexer(IDPDocument)
def category_indexer(obj):
    return IELANDocument(obj).category()

@indexer(IDPDocument)
def cat_path_indexer(obj):
    return IELANDocument(obj).cat_path()