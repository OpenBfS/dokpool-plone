from AccessControl.SecurityInfo import allow_class
from docpool.base.appregistry import APP_REGISTRY
from logging import getLogger
from plone import api
from plone.app.layout.viewlets.common import LogoViewlet
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import datetime


logger = getLogger(__name__)


class TimeViewlet(ViewletBase):
    index = ViewPageTemplateFile("time.pt")

    def get_local_time(self):
        return datetime.datetime.now()

    def get_utc_time(self):
        return datetime.datetime.now(datetime.UTC)


allow_class(TimeViewlet)


class LogoDocpoolViewlet(LogoViewlet):
    index = ViewPageTemplateFile("logo.pt")

    def getActiveApp(self):
        user = api.user.get_current()
        if not user:
            return {}
        active_app = user.getProperty("apps")
        if not active_app:
            return {}
        return APP_REGISTRY[active_app[0]]
