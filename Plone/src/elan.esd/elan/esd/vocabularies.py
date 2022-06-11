from AccessControl.SecurityInfo import allow_module
from docpool.base.utils import getDocumentPoolSite
from Products.CMFCore.utils import getToolByName
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class CategoryVocabulary:
    """
    """

    def __call__(self, context):
        # print context
        esd = getDocumentPoolSite(context)
        path = "/".join(esd.getPhysicalPath()) + "/esd"
        cat = getToolByName(esd, 'portal_catalog', None)
        if cat is None:
            return SimpleVocabulary([])

        items = sorted(
            (t.Title, t.getObject())
            for t in cat({"portal_type": "ELANDocCollection", "path": path})
        )
        items = [SimpleTerm(i[1], i[1], i[0]) for i in items]
        return SimpleVocabulary(items)


CategoryVocabularyFactory = CategoryVocabulary()


@implementer(IVocabularyFactory)
class CategoriesVocabulary:
    """
    """

    def __call__(self, context):
        # print context
        esd = getDocumentPoolSite(context)
        path = "/".join(esd.getPhysicalPath()) + "/esd"
        cat = getToolByName(esd, 'portal_catalog', None)
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
