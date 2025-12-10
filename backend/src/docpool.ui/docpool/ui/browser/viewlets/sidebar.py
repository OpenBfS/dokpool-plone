from docpool.base.utils import is_in_dp_folder
from plone.app.layout.viewlets import common
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.viewlet.interfaces import IViewletManager

import datetime


class ISidebarManager(IViewletManager):
    """Custom sidebar manager"""


class SidebarViewlet(common.ViewletBase):
    index = ViewPageTemplateFile("sidebar.pt")

    def render(self):
        # XXX Paths shouldn't be hard-coded. Maybe add a property to folders or introduce a behavior.
        if is_in_dp_folder(
            self.context,
            "content/Groups",
            "content/Transfers",
            "hintergrundinfos-ns",
        ):
            return ""
        return super().render()

    def get_local_time(self):
        return datetime.datetime.now()

    def get_utc_time(self):
        return datetime.datetime.now(datetime.UTC)

    def get_jst_time(self):
        return datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=8)
