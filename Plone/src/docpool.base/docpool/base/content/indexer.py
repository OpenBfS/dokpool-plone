from docpool.base.content.documentpool import IDocumentPool
from docpool.base.content.infodocument import IInfoDocument
from docpool.base.localbehavior.localbehavior import ILocalBehaviorSupport
from plone.dexterity.interfaces import IDexterityContainer
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer import indexer
from Products.CMFPlone.utils import base_hasattr


@indexer(IDocumentPool)
def docpool_apps_indexer(obj):
    try:
        return obj.supportedApps
    except BaseException:
        pass


@indexer(IDexterityContainer)
def container_apps_indexer(obj):
    """Used by most folders (including DPDocument)"""
    try:
        return ILocalBehaviorSupport(obj).local_behaviors
    except TypeError:
        return base_apps_indexer(obj)()


@indexer(IDexterityContent)
def base_apps_indexer(obj):
    if base_hasattr(obj, "APP"):
        return [obj.APP]


@indexer(IInfoDocument)
def infodoc_getIcon(obj):
    return None
