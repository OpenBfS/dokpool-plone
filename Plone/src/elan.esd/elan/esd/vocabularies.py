from AccessControl.SecurityInfo import allow_module
from docpool.base.utils import getDocumentPoolSite
from Products.CMFCore.utils import getToolByName
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class CategoryVocabulary(object):
    """    
    """

    implements(IVocabularyFactory)

    def __call__(self, context):
        # print context
        esd = getDocumentPoolSite(context)
        path = "/".join(esd.getPhysicalPath()) + "/esd"
        cat = getToolByName(esd, 'portal_catalog', None)
        if cat is None:
            return SimpleVocabulary([])

        items = [
            (t.Title, t.getObject())
            for t in cat({"portal_type": "ELANDocCollection", "path": path})
        ]
        items.sort()
        items = [SimpleTerm(i[1], i[1], i[0]) for i in items]
        return SimpleVocabulary(items)


CategoryVocabularyFactory = CategoryVocabulary()


class CategoriesVocabulary(object):
    """    
    """

    implements(IVocabularyFactory)

    def __call__(self, context):
        # print context
        esd = getDocumentPoolSite(context)
        path = "/".join(esd.getPhysicalPath()) + "/esd"
        cat = getToolByName(esd, 'portal_catalog', None)
        if cat is None:
            return SimpleVocabulary([])

        items = [
            (t.Title, t.getId)
            for t in cat({"portal_type": "ELANDocCollection", "path": path})
        ]
        items.sort()
        items = [SimpleTerm(i[1], i[1], i[0]) for i in items]
        return SimpleVocabulary(items)


CategoriesVocabularyFactory = CategoriesVocabulary()

# class ELANDocTypeVocabulary(object):
#     """
#     """
#     implements(IVocabularyFactory)
#
#     def __call__(self, context, raw=False):
#         esd = getELANSite(context)
#         path = "/".join(esd.getPhysicalPath()) + "/config"
#         cat = getToolByName(esd, 'portal_catalog', None)
#         if cat is None:
#             if not raw:
#                 return SimpleVocabulary([])
#             else:
#                 return []
#         types = cat({"portal_type":"DocType", "sort_on": "sortable_title", "path": path})
#          print len(types)
#         if not raw:
#             types = [ (brain.UID, brain.Title) for brain in types]
#         else:
#             types = [ (brain.getId, brain.Title) for brain in types]
#          print types
#         if not raw:
#             items = [SimpleTerm(i[0], i[0], i[1]) for i in types]
#             return SimpleVocabulary(items)
#         else:
#             return types
#
# ELANDocTypeVocabularyFactory = ELANDocTypeVocabulary()
#
# class ELANGroupDocTypeVocabulary(object):
#     """
#     """
#     implements(IVocabularyFactory)
#
#     def __call__(self, context):
#         types = getAllowedDocumentTypesForGroup(context)
#          print len(types)
#         types = [ (brain.getId, brain.Title) for brain in types]
#          print types
#         items = [SimpleTerm(i[0], i[0], i[1]) for i in types]
#         return SimpleVocabulary(items)
#
# ELANGroupDocTypeVocabularyFactory = ELANGroupDocTypeVocabulary()

# class ELANESDVocabulary(object):
#     """
#     """
#     implements(IVocabularyFactory)
#
#     def __call__(self, context, raw=False):
#         my_uid = None
#         if shasattr(context, "myDocumentPool", True):
#             my_uid = context.myDocumentPool().UID()
#
#         site = getSite()
#         cat = getToolByName(site, 'portal_catalog', None)
#         if cat is None:
#             if not raw:
#                 return SimpleVocabulary([])
#             else:
#                 return []
#         esds = cat.unrestrictedSearchResults({"portal_type":"DocumentPool", "sort_on": "sortable_title"})
#         # print len(types)
#         esds = [ (brain.UID, brain.Title) for brain in esds if brain.UID != my_uid]
#         # print types
#         if not raw:
#             items = [SimpleTerm(i[0], i[0], i[1]) for i in esds]
#             return SimpleVocabulary(items)
#         else:
#             return esds
#
# ELANESDVocabularyFactory = ELANESDVocabulary()
allow_module("elan.esd.vocabularies")
# allow_class(ELANESDVocabulary)
