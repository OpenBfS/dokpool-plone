# -*- coding: utf-8 -*-
from docpool.base.content.dpdocument import IDPDocument
from docpool.elan.config import ELAN_APP
from plone.indexer import indexer


@indexer(IDPDocument)
def scenarios_indexer(obj):
    try:
        return obj.doc_extension(ELAN_APP).scenarioIndex()
    except BaseException:
        return ['nonELANContent']


@indexer(IDPDocument)
def category_indexer(obj):
    try:
        return obj.doc_extension(ELAN_APP).category()
    except BaseException:
        pass


@indexer(IDPDocument)
def cat_path_indexer(obj):
    try:
        return obj.doc_extension(ELAN_APP).cat_path()
    except BaseException:
        pass
