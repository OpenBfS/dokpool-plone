from docpool.menu.utils import adaptQuery
from plone.app.layout.navigation.interfaces import (
    INavigationQueryBuilder,
    INavtreeStrategy,
)
from Products.CMFPlone.browser.navtree import (
    DefaultNavtreeStrategy,
    SitemapQueryBuilder,
)
from zope.interface import implementer

caching_strategy = "anonymous"  # FIXME: maybe cache individually?


@implementer(INavigationQueryBuilder)
class DropDownMenuQueryBuilder(SitemapQueryBuilder):
    def __init__(self, context):
        super().__init__(context)
        self.context = context
        # customize depth according to dropdown menu settings
        if "depth" in self.query["path"]:
            self.query["path"]["depth"] = 4

        adaptQuery(self.query, context)
        # print self.query


@implementer(INavtreeStrategy)
class DropDownMenuStrategy(DefaultNavtreeStrategy):
    def __init__(self, context, view=None):
        super().__init__(context, view)
        self.bottomLevel = 0
