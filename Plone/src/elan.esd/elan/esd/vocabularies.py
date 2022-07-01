from AccessControl.SecurityInfo import allow_module
from docpool.base.utils import getDocumentPoolSite
from plone.app.vocabularies.catalog import StaticCatalogVocabulary
from Products.CMFCore.utils import getToolByName
from zope.interface import implementer
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary


@provider(IVocabularyFactory)
def CategoryVocabularyFactory(context=None):
    """Used for Relationfield docpool.elan.behaviors.elandoctype.IELANDocType.contentCategory
    and elan.esd.portlets.collection.ICollectionPortlet.collection
    """
    esd = getDocumentPoolSite(context)
    path = "/".join(esd.getPhysicalPath()) + "/esd"
    return StaticCatalogVocabulary(
        {
            "portal_type": "ELANDocCollection",
            "sort_on": "sortable_title",
            "path": path,
        },
        title_template="{brain.Title}",
    )


@implementer(IVocabularyFactory)
class CategoriesVocabulary:
    """ """

    def __call__(self, context):
        # print context
        esd = getDocumentPoolSite(context)
        path = "/".join(esd.getPhysicalPath()) + "/esd"
        cat = getToolByName(esd, "portal_catalog", None)
        if cat is None:
            return SimpleVocabulary([])

        items = sorted(
            (t.Title, t.getId)
            for t in cat({"portal_type": "ELANDocCollection", "path": path})
        )
        items = [SimpleTerm(i[1], i[1], i[0]) for i in items]
        return SimpleVocabulary(items)


CategoriesVocabularyFactory = CategoriesVocabulary()


allow_module("elan.esd.vocabularies")
