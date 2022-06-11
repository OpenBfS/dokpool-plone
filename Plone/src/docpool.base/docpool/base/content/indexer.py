from docpool.base.config import BASE_APP
from docpool.base.content.documentpool import IDocumentPool
from docpool.base.content.dpdocument import IDPDocument
from docpool.base.content.infodocument import IInfoDocument
from docpool.localbehavior.localbehavior import ILocalBehaviorSupport
from plone.dexterity.interfaces import IDexterityContainer, IDexterityContent
from plone.indexer import indexer
from Products.CMFPlone.utils import base_hasattr


@indexer(IDPDocument)
def doc_apps_indexer(obj):
    # print "doc_apps_indexer", obj
    res = [BASE_APP]
    try:
        res.extend(ILocalBehaviorSupport(obj).local_behaviors)
    except BaseException:
        pass
    res.extend(base_apps_indexer(obj)())
    return list(set(res))


@indexer(IDocumentPool)
def docpool_apps_indexer(obj):
    try:
        return obj.supportedApps
    except BaseException:
        pass


@indexer(IDexterityContainer)
def container_apps_indexer(obj):
    # print "container_apps_indexer", obj
    try:
        res = ILocalBehaviorSupport(obj).local_behaviors
        return list(set(res))
    except BaseException:
        return base_apps_indexer(obj)


@indexer(IDexterityContent)
def base_apps_indexer(obj):
    # print "base_apps_indexer", obj
    if base_hasattr(obj, "APP"):
        return [obj.APP]
    else:
        return [BASE_APP]


@indexer(IInfoDocument)
def infodoc_getIcon(obj):
    return None
