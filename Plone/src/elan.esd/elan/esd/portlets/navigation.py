from Acquisition import aq_inner
from docpool.menu.utils import adaptQuery, getFoldersForCurrentUser
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.navtree import buildFolderTree
from plone.app.portlets.portlets import navigation
from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.browser.navtree import NavtreeQueryBuilder
from Products.CMFPlone.utils import base_hasattr
from zope.component import getMultiAdapter


class Renderer(navigation.Renderer):
    def __init__(self, context, request, view, manager, data):
        navigation.Renderer.__init__(self, context, request, view, manager, data)

    @memoize
    def getNavTree(self, _marker=[]):
        context = aq_inner(self.context)
        # Override by using a SitemapQueryBuilder so we get all nodes expanded
        queryBuilder = SitemapQueryBuilder(context)
        strategy = getMultiAdapter((context, self.data), INavtreeStrategy)

        if context.isPersonal():
            # Special treatment for the user's personal folders
            pfs = getFoldersForCurrentUser(context)
            return {"children": pfs}

        # Otherwise build the normal navigation
        ft = buildFolderTree(
            context, obj=context, query=queryBuilder(), strategy=strategy
        )
        # print ft
        return ft

    def navigation_root(self):
        if base_hasattr(self.context, "myDocumentPool"):
            return self.context.myDocumentPool()
        return self.getNavRoot()


class SitemapQueryBuilder(NavtreeQueryBuilder):
    """Build tree for ELAN Sitemap considering archive structures"""

    def __init__(self, context):
        NavtreeQueryBuilder.__init__(self, context)
        portal_url = getToolByName(context, "portal_url")
        portal_properties = getToolByName(context, "portal_properties")
        navtree_properties = getattr(portal_properties, "navtree_properties")
        sitemapDepth = navtree_properties.getProperty("sitemapDepth", 4)
        if (
            context.restrictedTraverse("@@context_helpers").is_archive()
            and not context.getId() == "archive"
        ):
            sitemapDepth += 3
        self.query["path"] = {
            "query": context.restrictedTraverse("@@context_helpers").is_archive()
            and not context.getId() == "archive"
            and "/".join(context.myELANArchive().getPhysicalPath())
            or portal_url.getPortalPath(),
            "depth": sitemapDepth,
        }
        adaptQuery(self.query, context)
