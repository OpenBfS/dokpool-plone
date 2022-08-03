from AccessControl.SecurityInfo import allow_class, allow_module
from docpool.base import DocpoolMessageFactory as _
from docpool.base.appregistry import activeApps, extendingApps, selectableApps
from docpool.base.content.doctype import IDocType
from docpool.base.utils import getAllowedDocumentTypesForGroup, getDocumentPoolSite
from plone import api
from plone.app.vocabularies.catalog import StaticCatalogVocabulary
from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from zope.component.hooks import getSite
from zope.interface import implementer
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary


@implementer(IVocabularyFactory)
class AvailableAppsVocabulary:
    """ """

    def __call__(self, context):
        dp_app_state = getMultiAdapter((context, context.REQUEST), name="dp_app_state")
        available = dp_app_state.appsPermittedForCurrentUser()
        return SimpleVocabulary(
            [
                SimpleTerm(app[0], title=_(app[1]))
                for app in activeApps()
                if app[0] in available
            ]
        )


AvailableAppsVocabularyFactory = AvailableAppsVocabulary()


@implementer(IVocabularyFactory)
class ActiveAppsVocabulary:
    """ """

    def __call__(self, context):

        return SimpleVocabulary(
            [SimpleTerm(app[0], title=_(app[1])) for app in activeApps()]
        )


ActiveAppsVocabularyFactory = ActiveAppsVocabulary()


@implementer(IVocabularyFactory)
class ExtendingAppsVocabulary:
    """ """

    def __call__(self, context):

        return SimpleVocabulary(
            [SimpleTerm(app[0], title=_(app[1])) for app in extendingApps()]
        )


ExtendingAppsVocabularyFactory = ExtendingAppsVocabulary()


@implementer(IVocabularyFactory)
class SelectableAppsVocabulary:
    """ """

    def __call__(self, context):

        return SimpleVocabulary(
            [SimpleTerm(app[0], title=_(app[1])) for app in selectableApps()]
        )


SelectableAppsVocabularyFactory = SelectableAppsVocabulary()


@implementer(IVocabularyFactory)
class DTOptionsVocabulary:
    """ """

    def __call__(self, context):
        # print context
        if not context:
            return []
        return SimpleVocabulary(
            [SimpleTerm(dt[0], title=dt[1]) for dt in context.getMatchingDocTypes()]
        )


DTOptionsVocabularyFactory = DTOptionsVocabulary()


@implementer(IVocabularyFactory)
class DocumentTypesVocabulary:
    """ """

    def __call__(self, context):
        esd = getDocumentPoolSite(context)
        path = "/".join(esd.getPhysicalPath()) + "/config"
        cat = getToolByName(esd, "portal_catalog", None)
        if cat is None:
            return SimpleVocabulary([])

        items = [(t.Title, t.id) for t in cat({"portal_type": "DocType", "path": path})]
        items.extend(
            [
                ("infodoc", "infodoc"),
                ("active", "active"),
                ("inactive", "inactive"),
                ("closed", "closed"),
            ]
        )
        items.sort()
        items = [SimpleTerm(i[1], i[1], i[0]) for i in items]
        return SimpleVocabulary(items)


DocumentTypesVocabularyFactory = DocumentTypesVocabulary()


@provider(IVocabularyFactory)
def DocTypeVocabularyFactory(context=None, raw=False):
    """Used for Relationfield docpool.base.content.doctype.IDocType.allowedDocTypes
    and in docpool.base.monkey.possibleDocTypes
    """
    esd = getDocumentPoolSite(context)
    path = "/".join(esd.getPhysicalPath()) + "/config"
    query = {
        "object_provides": IDocType.__identifier__,
        "sort_on": "sortable_title",
        "path": path,
    }
    if raw:
        brains = api.content.find(**query)
        return [(brain.getId, brain.Title) for brain in brains]
    return StaticCatalogVocabulary(query, title_template="{brain.Title}")


@implementer(IVocabularyFactory)
class GroupDocTypeVocabulary:
    """ """

    def __call__(self, context):
        types = getAllowedDocumentTypesForGroup(context)
        # print len(types)
        types = [(brain.getId, brain.Title) for brain in types]
        # print types
        items = [SimpleTerm(i[0], i[0], i[1]) for i in types]
        return SimpleVocabulary(items)


GroupDocTypeVocabularyFactory = GroupDocTypeVocabulary()


@implementer(IVocabularyFactory)
class DocumentPoolVocabulary:
    """ """

    def __call__(self, context, raw=False):
        my_uid = None
        if getattr(context, "myDocumentPool", None) is not None:
            my_uid = context.myDocumentPool().UID()

        site = getSite()
        cat = getToolByName(site, "portal_catalog", None)
        if cat is None:
            if not raw:
                return SimpleVocabulary([])
            else:
                return []
        esds = cat.unrestrictedSearchResults(
            {"portal_type": "DocumentPool", "sort_on": "sortable_title"}
        )
        # print len(esds)
        esds = [(brain.UID, brain.Title) for brain in esds if brain.UID != my_uid]
        # print esds
        if not raw:
            items = [SimpleTerm(i[0], i[0], i[1]) for i in esds]
            return SimpleVocabulary(items)
        else:
            return esds


DocumentPoolVocabularyFactory = DocumentPoolVocabulary()


@implementer(IVocabularyFactory)
class UserDocumentPoolVocabulary:
    """ """

    def __call__(self, context, raw=False):

        site = getSite()
        cat = getToolByName(site, "portal_catalog", None)
        if cat is None:
            if not raw:
                return SimpleVocabulary([])
            else:
                return []
        esds = cat.unrestrictedSearchResults(
            {"portal_type": "DocumentPool", "sort_on": "sortable_title"}
        )
        # print len(esds)
        esds = [(brain.UID, brain.Title) for brain in esds]
        # print esds
        if not raw:
            items = [SimpleTerm(i[0], i[0], i[1]) for i in esds]
            return SimpleVocabulary(items)
        else:
            return esds


UserDocumentPoolVocabularyFactory = UserDocumentPoolVocabulary()


@implementer(IVocabularyFactory)
class DashboardCollectionsVocabulary:
    def __call__(self, context, raw=False):
        # print context
        esd = getDocumentPoolSite(context)
        path = "/".join(esd.getPhysicalPath()) + "/contentconfig"
        cat = getToolByName(esd, "portal_catalog", None)
        if cat is None:
            if not raw:
                return SimpleVocabulary([])
            else:
                return []
        types = cat(
            {
                "portal_type": "DashboardCollection",
                "sort_on": "sortable_title",
                "path": path,
            }
        )
        if not raw:
            types = [(brain.getObject(), brain.Title) for brain in types]
        else:
            types = [(brain.getId, brain.Title) for brain in types]

        if not raw:
            items = [SimpleTerm(i[0], i[0], i[1]) for i in types]
            return SimpleVocabulary(items)
        else:
            return types


DashboardCollectionsVocabularyFactory = DashboardCollectionsVocabulary()

allow_module("docpool.base.vocabularies")
allow_class(DocumentPoolVocabulary)
