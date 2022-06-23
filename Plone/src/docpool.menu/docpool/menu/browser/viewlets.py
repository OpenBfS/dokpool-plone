from time import time

from Acquisition import aq_inner
from docpool.menu.browser.menu import DropDownMenuQueryBuilder, caching_strategy
from docpool.menu.utils import (
    getApplicationDocPoolsForCurrentUser,
    getFoldersForCurrentUser,
)
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.navtree import buildFolderTree
from plone.app.layout.viewlets import common
from plone.memoize import ram
from plone.memoize.compress import xhtmlslimmer
from Products.CMFPlone.i18nl10n import utranslate
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter


def menu_cache_key(f, view):
    # menu cache key conssits of:
    # - path to selected item
    # - site can be accessed on different domains
    # - language is important for multilingua sites

    portal_state = getMultiAdapter(
        (view.context, view.request), name="plone_portal_state"
    )
    site_len = len(portal_state.navigation_root_path().split("/"))
    content_path = view.context.getPhysicalPath()[site_len:]
    path_key = view.request.physicalPathToURL(content_path)

    language = portal_state.locale().getLocaleID()

    # Cache for five minutes. Note that the HTTP RAM-cache
    # typically purges entries after 60 minutes.
    return view.__name__ + path_key + language + str(time() // (60 * 5))


def dropdowncache(f):
    def func(view):
        portal_state = getMultiAdapter(
            (view.context, view.request), name="plone_portal_state"
        )
        # it is impossible to reliably cache entire rendered menu generated
        # with potral actions strategy.
        if not portal_state.anonymous() and caching_strategy == "anonymous":
            return f(view)
        return ram.cache(menu_cache_key)(f)(view)

    return func


class GlobalSectionsViewlet(common.GlobalSectionsViewlet):
    index = ViewPageTemplateFile("templates/sections.pt")
    recurse = ViewPageTemplateFile("templates/sections_recurse.pt")

    def portal_tabs(self):
        tabs = self._content_tabs()

        for tab in tabs:
            if tab["id"].find("config") != -1:
                tab["item_class"] = "config"
            elif tab["id"] == "content":
                tab["item_class"] = "hide"

        apds = getApplicationDocPoolsForCurrentUser(self.context)
        if apds:
            apds.extend(tabs)
            tabs = apds

        if not self.context.restrictedTraverse("@@context_helpers").is_archive():
            ffu = getFoldersForCurrentUser(self.context)
            if ffu:
                for f in ffu:
                    if "item_class" not in f:
                        f["item_class"] = "personal"
                tabs.append(
                    {
                        "id": "content",
                        "Title": utranslate(
                            "docpool.base", "Content Area", context=self.context
                        ),
                        "Description": "",
                        "getURL": "",
                        "show_children": True,
                        "children": ffu,
                        "currentItem": False,
                        "item_class": "contentarea",
                        "currentParent": self.context.isPersonal(),
                        "normalized_review_state": "visible",
                    }
                )
        return tabs

    def _content_tabs(self):
        """Return tree of tabs based on content structure"""
        context = aq_inner(self.context)

        queryBuilder = DropDownMenuQueryBuilder(context)
        strategy = getMultiAdapter((context, None), INavtreeStrategy)
        # XXX This works around a bug in plone.app.portlets which was
        # fixed in http://dev.plone.org/svn/plone/changeset/18836
        # When a release with that fix is made this workaround can be
        # removed and the plone.app.portlets requirement in setup.py
        # be updated.
        if strategy.rootPath is not None and strategy.rootPath.endswith("/"):
            strategy.rootPath = strategy.rootPath[:-1]

        return buildFolderTree(
            context, obj=context, query=queryBuilder(), strategy=strategy
        ).get("children", [])

    @dropdowncache
    def createMenu(self):
        html = self.recurse(children=self.portal_tabs(), level=1)
        return xhtmlslimmer.compress(html).strip(" \n")
