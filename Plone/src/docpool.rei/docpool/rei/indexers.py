# -*- coding: utf-8 -*-
from docpool.base.content.dpdocument import IDPDocument
from docpool.rei.config import REI_APP
from plone.indexer import indexer


@indexer(IDPDocument)
def report_year(obj):
    try:
        return obj.doc_extension(REI_APP).Year
    except BaseException:
        pass
