from plone.app.layout.viewlets.common import PathBarViewlet, ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter


class PathBarViewlet(ViewletBase):
    index = ViewPageTemplateFile("path_bar.pt")

    def update(self):
        super().update()

        self.is_rtl = self.portal_state.is_rtl()

        breadcrumbs_view = getMultiAdapter(
            (self.context, self.request), name="breadcrumbs_view"
        )
        self.breadcrumbs = breadcrumbs_view.breadcrumbs()
