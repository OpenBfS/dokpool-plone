# -*- coding: utf-8 -*-
from zope.interface import implements

from Products.CMFPlone.browser.navtree import SitemapQueryBuilder
from Products.CMFPlone.browser.navtree import DefaultNavtreeStrategy

from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.interfaces import INavigationQueryBuilder

from docpool.menu.utils import adaptQuery

show_content_tabs = True
show_actions_tabs = False
content_before_actions_tabs = True
actions_category = None
enable_caching = True
content_tabs_level = 0
caching_strategy = 'anonymous' # FIXME: maybe cache individually?
nested_category_sufix = ''
nested_category_prefix = ''
actions_tabs_level = 0
show_nonfolderish_tabs = True

class DropDownMenuQueryBuilder(SitemapQueryBuilder):

    implements(INavigationQueryBuilder)

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


class DropDownMenuStrategy(DefaultNavtreeStrategy):

    implements(INavtreeStrategy)

    def __init__(self, context, view=None):
        super(DropDownMenuStrategy, self).__init__(context, view)
        self.bottomLevel = content_tabs_level

