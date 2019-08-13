# -*- coding: utf-8 -*-
from docpool.menu.utils import adaptQuery
from plone.app.layout.navigation.interfaces import INavigationQueryBuilder
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from Products.CMFPlone.browser.navtree import DefaultNavtreeStrategy
from Products.CMFPlone.browser.navtree import SitemapQueryBuilder
from zope.interface import implementer


show_content_tabs = True
show_actions_tabs = False
content_before_actions_tabs = True
actions_category = None
enable_caching = True
content_tabs_level = 0
caching_strategy = 'anonymous'  # FIXME: maybe cache individually?
nested_category_sufix = ''
nested_category_prefix = ''
actions_tabs_level = 0
show_nonfolderish_tabs = True


@implementer(INavigationQueryBuilder)
class DropDownMenuQueryBuilder(SitemapQueryBuilder):

    def __init__(self, context):
        super(DropDownMenuQueryBuilder, self).__init__(context)
        self.context = context
        # customize depth according to dropdown menu settings
        if content_tabs_level > 0:
            self.query['path']['depth'] = content_tabs_level
        elif 'depth' in self.query['path']:
            self.query['path']['depth'] = 4

        # constrain non-folderish objects if required
        if not show_nonfolderish_tabs:
            self.query['is_folderish'] = True
        adaptQuery(self.query, context)
        # print self.query


@implementer(INavtreeStrategy)
class DropDownMenuStrategy(DefaultNavtreeStrategy):

    def __init__(self, context, view=None):
        super(DropDownMenuStrategy, self).__init__(context, view)
        self.bottomLevel = content_tabs_level
