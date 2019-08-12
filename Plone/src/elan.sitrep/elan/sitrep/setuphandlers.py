# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
class args:
    def __init__(self, **kw):
        self.__dict__.update(kw)

def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('elan.sitrep_various.txt') is None:
        return
    # Add additional setup code here
    cat = getToolByName(context.getSite(), 'sr_catalog')
    # Add indexes and metadatas
    for index_name, index_type, extra in cat.enumerateIndexes():
        try:
            if index_name not in cat.indexes():
                if index_type == 'ZCTextIndex':
                    extra = args(doc_attr=index_name,
                                 lexicon_id='pg_lexicon',
                                 index_type='Okapi BM25 Rank')
                    cat.addIndex(index_name, index_type, extra=extra)
                else:
                    if extra:
                        extra = args(indexed_attrs=extra)
                    cat.addIndex(index_name, index_type, extra=extra)

            if not index_name in cat.schema():
                cat.addColumn(index_name)
        except:
            pass    # for metadata
