# -*- coding: utf-8 -*-
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer import indexer
from Products.CMFPlone import log
from docpool.base.content.dpdocument import IDPDocument
from docpool.base.content.documentpool import IDocumentPool
from docpool.base.config import BASE_APP
from docpool.base.interfaces import IApplicationAware


@indexer(IDPDocument)
def doc_apps_indexer(obj):
    try:
        return [ 'elan', 'transfers' ] # FIXME:
    except:
        pass


@indexer(IDocumentPool)
def docpool_apps_indexer(obj):
    try:
        return [ obj.supportedApps ]
    except:
        pass

@indexer(IDexterityContent)
def base_apps_indexer(obj):
    return [ BASE_APP ]

@indexer(IApplicationAware)
def apps_aware_indexer(obj):
    return [ obj.APP or BASE_APP ]