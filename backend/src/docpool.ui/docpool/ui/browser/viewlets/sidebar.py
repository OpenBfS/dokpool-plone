from plone.app.layout.viewlets import common
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.viewlet.interfaces import IViewletManager

import datetime


class ISidebarManager(IViewletManager):
    """Custom sidebar manager"""


class SidebarViewlet(common.ViewletBase):
    index = ViewPageTemplateFile("sidebar.pt")

    def get_local_time(self):
        return datetime.datetime.now()

    def get_utc_time(self):
        return datetime.datetime.now(datetime.UTC)

    def get_jst_time(self):
        return datetime.datetime.now(datetime.UTC) + datetime.timedelta(hours=8)
