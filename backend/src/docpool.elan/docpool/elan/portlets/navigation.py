from Acquisition import aq_inner
from docpool.base.browser.viewlets.menu import adaptQuery
from docpool.base.browser.viewlets.menu import getFoldersForCurrentUser
from docpool.base.content.archiving import IArchiving
from docpool.base.utils import is_personal
from plone import api
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.navtree import buildFolderTree
from plone.app.portlets.portlets import navigation
from plone.memoize.instance import memoize
from Products.CMFPlone.browser.navtree import NavtreeQueryBuilder
from Products.CMFPlone.utils import base_hasattr
from zope.component import getMultiAdapter


class Renderer(navigation.Renderer):
    def __init__(self, context, request, view, manager, data):
        navigation.Renderer.__init__(self, context, request, view, manager, data)

    @memoize
    def getNavTree(self, _marker=None):
        if _marker is None:
            _marker = []
        context = aq_inner(self.context)

        if is_personal(context):
            # Special treatment for the user's personal folders
            pfs = getFoldersForCurrentUser(context)
            return {"children": pfs or []}

        # Override by using a SitemapQueryBuilder so we get all nodes expanded
        queryBuilder = SitemapQueryBuilder(context)

        # Otherwise build the normal navigation
        strategy = getMultiAdapter((context, self.data), INavtreeStrategy)
        ft = buildFolderTree(context, obj=context, query=queryBuilder(), strategy=strategy)
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
        if IArchiving(context).is_archive and context.getId() != "archive":
            path = "/".join(context.myELANArchive().getPhysicalPath())
            sitemap_depth = 7
        else:
            path = "/".join(api.portal.get().getPhysicalPath())
            sitemap_depth = 4
        self.query["path"] = {
            "query": path,
            "depth": sitemap_depth,
        }
        adaptQuery(self.query, context)
