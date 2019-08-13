# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from docpool.menu.utils import getApplicationDocPoolsForCurrentUser
from docpool.menu.utils import getFoldersForCurrentUser
from menu import actions_category
from menu import actions_tabs_level
from menu import caching_strategy
from menu import content_before_actions_tabs
from menu import content_tabs_level
from menu import DropDownMenuQueryBuilder
from menu import enable_caching
from menu import nested_category_prefix
from menu import nested_category_sufix
from menu import show_actions_tabs
from menu import show_content_tabs
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.navtree import buildFolderTree
from plone.app.layout.viewlets import common
from plone.memoize import ram
from plone.memoize.compress import xhtmlslimmer
from Products.CMFCore.ActionInformation import ActionInfo
from Products.CMFCore.interfaces import IAction
from Products.CMFCore.interfaces import IActionCategory
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.i18nl10n import utranslate
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from time import time
from zope.component import getMultiAdapter

import copy


def menu_cache_key(f, view):
    # menu cache key conssits of:
    # - path to selected item
    # - site can be accessed on different domains
    # - language is important for multilingua sites

    portal_state = getMultiAdapter(
        (view.context, view.request), name=u'plone_portal_state'
    )
    site_len = len(portal_state.navigation_root_path().split('/'))
    content_path = view.context.getPhysicalPath()[site_len:]
    if content_tabs_level > 0:
        content_path = content_path[:content_tabs_level]
    path_key = view.request.physicalPathToURL(content_path)

    language = portal_state.locale().getLocaleID()

    # Cache for five minutes. Note that the HTTP RAM-cache
    # typically purges entries after 60 minutes.
    return view.__name__ + path_key + language + str(time() // (60 * 5))


# we are caching the menu structure built out of portal_actions tool
# this cache key does not take in account expressions and roles settings
def tabs_cache_key(f, view, site_url):
    portal_state = getMultiAdapter(
        (view.context, view.request), name=u'plone_portal_state'
    )
    language = portal_state.locale().getLocaleID()
    return site_url + language + str(time() // (60 * 60))


def dropdowncache(f):
    def func(view):
        portal_state = getMultiAdapter(
            (view.context, view.request), name=u'plone_portal_state'
        )
        # it is impossible to reliably cache entire rendered menu generated
        # with potral actions strategy.
        if (
            not enable_caching
            or show_actions_tabs
            or (not portal_state.anonymous() and caching_strategy == 'anonymous')
        ):
            return f(view)
        return ram.cache(menu_cache_key)(f)(view)

    return func


def tabscache(f):
    def func(view, site_url):
        if not enable_caching:
            return f(view, site_url)
        return ram.cache(tabs_cache_key)(f)(view, site_url)

    return func


class GlobalSectionsViewlet(common.GlobalSectionsViewlet):
    index = ViewPageTemplateFile('templates/sections.pt')
    recurse = ViewPageTemplateFile('templates/sections_recurse.pt')

    def update(self):
        # we may need some previously defined variables
        # super(GlobalSectionsViewlet, self).update()

        # prepare to gather portal tabs
        context = aq_inner(self.context)
        self.tool = getToolByName(context, 'portal_actions')
        plone_portal_state = getMultiAdapter(
            (self.context, self.request), name="plone_portal_state"
        )
        self.site_url = plone_portal_state.navigation_root_url()
        context_state = getMultiAdapter(
            (self.context, self.request), name="plone_context_state"
        )
        self.context_url = (
            context_state.is_default_page()
            and '/'.join(self.context.absolute_url().split('/')[:-1])
            or self.context.absolute_url()
        )

        self.cat_sufix = nested_category_sufix or ''
        self.cat_prefix = nested_category_prefix or ''

    def portal_tabs(self):
        tabs = []

        # fetch actions-based tabs?
        if show_actions_tabs:
            tabs.extend(self._actions_tabs())

        # fetch content structure-based tabs?
        if show_content_tabs:
            # put content-based actions before content structure-based ones?
            if content_before_actions_tabs:
                tabs = self._content_tabs() + tabs
            else:
                tabs.extend(self._content_tabs())

        for tab in tabs:
            if tab['id'].find('config') != -1:
                tab['item_class'] = "config"
            elif tab['id'] == 'content':
                tab['item_class'] = "hide"

        apds = getApplicationDocPoolsForCurrentUser(self.context)
        if apds:
            apds.extend(tabs)
            tabs = apds

        if not self.context.isArchive():
            ffu = getFoldersForCurrentUser(self.context)
            if ffu:
                for f in ffu:
                    if 'item_class' not in f:
                        f['item_class'] = "personal"
                tabs.append(
                    {
                        'id': 'content',
                        'Title': utranslate(
                            "docpool.base", "Content Area", context=self.context
                        ),
                        'Description': '',
                        'getURL': '',
                        'show_children': True,
                        'children': ffu,
                        'currentItem': False,
                        'item_class': 'contentarea',
                        'currentParent': self.context.isPersonal(),
                        'normalized_review_state': 'visible',
                    }
                )
        return tabs

    def _actions_tabs(self):
        """Return tree of tabs based on portal_actions tool configuration"""
        conf = self.conf
        tool = self.tool
        url = self.context_url
        starts = url.startswith

        # check if we have required root actions category inside tool
        if actions_category not in tool.objectIds():
            return []
        listtabs = []
        res, listtabs = self.prepare_tabs(self.site_url)
        res = copy.deepcopy(res)
        self.tabs = listtabs

        # if there is no custom menu in portal tabs return
        if not listtabs:
            return []

        current_item = -1
        delta = 1000
        for info in listtabs:
            if starts(info['url']) and len(url) - len(info['url']) < delta:
                delta = len(self.context_url) - len(info['url'])
                current_item = listtabs.index(info)
        self.id_chain = []

        active = listtabs[current_item]['url'] == self.site_url
        active = active and self.context_url == self.site_url
        active = listtabs[current_item]['url'] != self.site_url or active
        if current_item > -1 and current_item < len(listtabs) and active:
            self.mark_active(
                listtabs[current_item]['id'], listtabs[current_item]['url']
            )
        self._activate(res)
        return res

    @tabscache
    def prepare_tabs(self, site_url):
        def normalize_actions(category, object, level, parent_url=None):
            """walk through the tabs dictionary and build list of all tabs"""
            tabs = []
            for info in self._actionInfos(category, object):
                icon = info['icon'] and '<img src="%s" />' % info['icon'] or ''
                children = []
                bottomLevel = actions_tabs_level
                if bottomLevel < 1 or level < bottomLevel:
                    # try to find out appropriate subcategory
                    subcat_id = self.cat_prefix + info['id'] + self.cat_sufix
                    in_category = subcat_id in category.objectIds()
                    if subcat_id != info['id'] and in_category:
                        subcat = category._getOb(subcat_id)
                        if IActionCategory.providedBy(subcat):
                            children = normalize_actions(
                                subcat, object, level + 1, info['url']
                            )

                parent_id = category.getId()
                parent_id = parent_id.replace(self.cat_prefix, '')
                parent_id = parent_id.replace(self.cat_sufix, '')
                tab = {
                    'id': info['id'],
                    'title': info['title'],
                    'url': info['url'],
                    'parent': (parent_id, parent_url),
                }
                tabslist.append(tab)

                tab = {
                    'id': info['id'],
                    'Title': info['title'],
                    'Description': info['description'],
                    'getURL': info['url'],
                    'show_children': len(children) > 0,
                    'children': children,
                    'currentItem': False,
                    'currentParent': False,
                    'item_icon': {'html_tag': icon},
                    'normalized_review_state': 'visible',
                }
                tabs.append(tab)
            return tabs

        tabslist = []
        tabs = normalize_actions(
            self.tool._getOb(actions_category), aq_inner(self.context), 0
        )
        return tabs, tabslist

    def _activate(self, res):
        """Mark selected chain in the tabs dictionary"""
        for info in res:
            if info['getURL'] in self.id_chain:
                info['currentItem'] = True
                info['currentParent'] = True
                if info['children']:
                    self._activate(info['children'])

    def mark_active(self, current_id, url):
        for info in self.tabs:
            if info['id'] == current_id and info['url'] == url:
                self.mark_active(info['parent'][0], info['parent'][1])
                self.id_chain.append(info['url'])

    def _actionInfos(
        self,
        category,
        object,
        check_visibility=1,
        check_permissions=1,
        check_condition=1,
        max=-1,
    ):
        """Return action infos for a given category"""
        ec = self.tool._getExprContext(object)
        actions = [
            ActionInfo(action, ec)
            for action in category.objectValues()
            if IAction.providedBy(action)
        ]

        action_infos = []
        for ai in actions:
            if check_visibility and not ai['visible']:
                continue
            if check_permissions and not ai['allowed']:
                continue
            if check_condition and not ai['available']:
                continue
            action_infos.append(ai)
            if max + 1 and len(action_infos) >= max:
                break
        return action_infos

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
        ).get('children', [])

    @dropdowncache
    def createMenu(self):
        html = self.recurse(children=self.portal_tabs(), level=1)
        return xhtmlslimmer.compress(html).strip(' \n')
