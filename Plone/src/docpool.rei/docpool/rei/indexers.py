from docpool.base.content.dpdocument import IDPDocument
from docpool.rei.config import REI_APP
from plone.indexer import indexer


@indexer(IDPDocument)
def report_year(obj):
    try:
        return str(obj.doc_extension(REI_APP).Year)
    except TypeError:
        pass
    return ''
