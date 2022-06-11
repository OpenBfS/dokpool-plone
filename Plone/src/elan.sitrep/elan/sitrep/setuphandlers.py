from plone import api


class args:
    def __init__(self, **kw):
        self.__dict__.update(kw)


def post_install(context):
    cat = api.portal.get_tool("sr_catalog")
    # Add indexes and metadatas
    for index_name, index_type, extra in cat.enumerateIndexes():
        try:
            if index_name not in cat.indexes():
                if index_type == "ZCTextIndex":
                    extra = args(
                        doc_attr=index_name,
                        lexicon_id="pg_lexicon",
                        index_type="Okapi BM25 Rank",
                    )
                    cat.addIndex(index_name, index_type, extra=extra)
                else:
                    if extra:
                        extra = args(indexed_attrs=extra)
                    cat.addIndex(index_name, index_type, extra=extra)

            if not index_name in cat.schema():
                cat.addColumn(index_name)
        except BaseException:
            pass  # for metadata
