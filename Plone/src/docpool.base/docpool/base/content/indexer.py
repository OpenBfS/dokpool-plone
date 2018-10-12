# -*- coding: utf-8 -*-
from Products.Archetypes.utils import shasattr
from plone.dexterity.interfaces import IDexterityContent, IDexterityContainer
from plone.indexer import indexer
from Products.CMFPlone import log
from docpool.base.content.dpdocument import IDPDocument
from docpool.base.content.documentpool import IDocumentPool
from docpool.base.config import BASE_APP
from docpool.localbehavior.localbehavior import ILocalBehaviorSupport


@indexer(IDocumentPool)
def docpool_apps_indexer(obj):
    #print "docpool_apps_indexer"
    try:
        return obj.supportedApps
    except:
        pass

@indexer(IDexterityContainer)
def container_apps_indexer(obj):
    #print "container_apps_indexer", obj
    res = []
    try:
        res = ILocalBehaviorSupport(obj).local_behaviors
    except:
        pass
    #print res
    res.extend(base_apps_indexer(obj)())
    return list(set(res))

@indexer(IDexterityContent)
def base_apps_indexer(obj):
    #print "base_apps_indexer", obj
    if shasattr(obj, "APP"):
        #print obj.APP
        return [ obj.APP ]
    else:
        #print "base only"
        return [ BASE_APP ]

