from docpool.base.content.dpdocument import IDPDocument
from docpool.rei.behaviors.reidoc import IREIDoc
from plone.indexer import indexer


# TODO: Remove after upgrade to Python 3
@indexer(IDPDocument)
def Origins(obj):
    reidoc = IREIDoc(obj, None)
    if not reidoc:
        return
    if not reidoc.Origins:
        return []
    return reidoc.Origins
