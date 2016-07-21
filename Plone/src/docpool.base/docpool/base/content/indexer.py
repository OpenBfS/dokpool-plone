# -*- coding: utf-8 -*-
from Products.Archetypes.utils import shasattr
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer import indexer
from Products.CMFPlone import log
from docpool.base.content.dpdocument import IDPDocument
from docpool.base.content.documentpool import IDocumentPool
from docpool.base.config import BASE_APP
from docpool.localbehavior.localbehavior import ILocalBehaviorSupport


@indexer(IDPDocument)
def doc_apps_indexer(obj):
    try:
        res = [ BASE_APP ]
        res.extend(ILocalBehaviorSupport(obj).local_behaviors)
        return res
    except:
        pass


@indexer(IDocumentPool)
def docpool_apps_indexer(obj):
    try:
        return obj.supportedApps
    except:
        pass

@indexer(IDexterityContent)
def base_apps_indexer(obj):
    if shasattr(obj, "APP"):
        return [ obj.APP ]
    else:
        return [ BASE_APP ]
