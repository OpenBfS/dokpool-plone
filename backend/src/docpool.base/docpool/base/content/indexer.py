from docpool.base.content.doctype import IDocType
from docpool.base.content.documentpool import IDocumentPool
from docpool.base.content.dpdocument import IDPDocument
from docpool.base.content.dptransferfolder import IDPTransferFolder
from docpool.base.content.groupfolder import IGroupFolder
from docpool.base.content.infodocument import IInfoDocument
from docpool.base.content.userfolder import IUserFolder
from docpool.base.localbehavior.localbehavior import ILocalBehaviorSupport
from plone.dexterity.interfaces import IDexterityContent
from plone.indexer import indexer
from Products.CMFPlone.utils import base_hasattr


@indexer(IDocumentPool)
def docpool_apps_supported(obj):
    try:
        return obj.supportedApps
    except BaseException:
        pass


@indexer(IDexterityContent)
def apps_supported(obj):
    # Registering a indexer more specific for ILocalBehaviorSupporting will fail
    # during clear & rebuild of the catalog. The indexer-lookup uses a object-based
    # cache in get_assignable that sometimes not yet finds DexterityLocalBehaviorAssignable.
    # So we register the indexer more generally and check for ILocalBehaviorSupport only here.
    try:
        return ILocalBehaviorSupport(obj).local_behaviors
    except TypeError:
        pass
    if base_hasattr(obj, "APP"):
        return [obj.APP]


@indexer(IInfoDocument)
def infodoc_getIcon(obj):
    return None


@indexer(IDPDocument)
def group(obj):
    for item in obj.aq_chain:
        if IGroupFolder.providedBy(item):
            return item.UID()
        elif IDPTransferFolder.providedBy(item):
            return item.UID()
        elif IUserFolder.providedBy(item):
            return item.UID()


@indexer(IDPDocument)
def subcategory_dpdocument(obj):
    return obj.subcategory()


@indexer(IDocType)
def subcategory_doctype(obj):
    return obj.subcategory()


@indexer(IDPDocument)
def category_dpdocument(obj):
    return obj.category()


@indexer(IDocType)
def category_doctype(obj):
    return obj.category()
