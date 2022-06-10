# -*- coding: utf-8 -*-
from docpool.base.content.dpdocument import IDPDocument
from docpool.elan.behaviors.elandocument import IELANDocument
from docpool.elan.config import ELAN_APP
from plone.indexer import indexer
from Products.CMFPlone.utils import safe_encode

import six


@indexer(IDPDocument)
def scenarios_indexer(obj):
    try:
        return obj.doc_extension(ELAN_APP).scenarioIndex()
    except BaseException:
        return ['nonELANContent']


@indexer(IDPDocument)
def category_indexer(obj):
    elandoc = IELANDocument(obj, None)
    if not elandoc:
        return
    categories = elandoc.category()
    return categories


@indexer(IDPDocument)
def cat_path_indexer(obj):
    try:
        return obj.doc_extension(ELAN_APP).cat_path()
    except BaseException:
        pass
