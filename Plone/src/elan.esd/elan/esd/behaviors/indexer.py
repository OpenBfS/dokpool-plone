from docpool.base.content.dpdocument import IDPDocument
from docpool.elan.behaviors.elandocument import IELANDocument
from plone.indexer import indexer


@indexer(IDPDocument)
def scenarios_indexer(obj):
    try:
        return IELANDocument(obj).scenarioIndex()
    except BaseException:
        pass


@indexer(IDPDocument)
def category_indexer(obj):
    try:
        return IELANDocument(obj).category()
    except BaseException:
        pass


@indexer(IDPDocument)
def cat_path_indexer(obj):
    try:
        return IELANDocument(obj).cat_path()
    except BaseException:
        pass
