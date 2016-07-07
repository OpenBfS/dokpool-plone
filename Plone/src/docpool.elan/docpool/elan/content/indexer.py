# -*- coding: utf-8 -*-
from plone.indexer import indexer
from Products.CMFPlone import log
from docpool.base.content.dpdocument import IDPDocument
from docpool.elan.config import ELAN_APP

@indexer(IDPDocument)
def scenarios_indexer(obj):
    try:
        return obj.doc_extension(ELAN_APP).scenarioIndex()
    except:
        pass

@indexer(IDPDocument)
def category_indexer(obj):
    try:
        return obj.doc_extension(ELAN_APP).category()
    except:
        pass

@indexer(IDPDocument)
def cat_path_indexer(obj):
    try:
        return obj.doc_extension(ELAN_APP).cat_path()
    except:
        pass