from docpool.base.content.documentpool import IDocumentPool
from docpool.base.content.infodocument import IInfoDocument
from docpool.base.localbehavior.localbehavior import ILocalBehaviorSupport
from docpool.base.localbehavior.localbehavior import ILocalBehaviorSupporting
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer import indexer
from Products.CMFPlone.utils import base_hasattr


@indexer(IDocumentPool)
def docpool_apps_indexer(obj):
    try:
        return obj.supportedApps
    except BaseException:
        pass


@indexer(ILocalBehaviorSupporting)
def local_behaviors_apps_indexer(obj):
    try:
        return ILocalBehaviorSupport(obj).local_behaviors
    except TypeError:
        # This only happends sometimes during test-setup.
        pass


@indexer(IDexterityContent)
def base_apps_indexer(obj):
    if base_hasattr(obj, "APP"):
        return [obj.APP]


@indexer(IInfoDocument)
def infodoc_getIcon(obj):
    return None
