# -*- coding: utf-8 -*-
from plone.indexer import indexer
from Products.CMFPlone import log
from docpool.base.content.dpdocument import IDPDocument
from docpool.doksys.config import DOKSYS_APP

@indexer(IDPDocument)
def network_operator_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).network_operator
    except:
        pass

