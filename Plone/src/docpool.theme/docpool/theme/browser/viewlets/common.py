import plone.api as api
from AccessControl.SecurityInfo import allow_class, allow_module
from docpool.base.appregistry import APP_REGISTRY
from plone.app.layout.viewlets.common import LogoViewlet, ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

allow_module("elan.esd.browser")
allow_module("elan.esd.browser.viewlets")
allow_module("elan.esd.browser.viewlets.common")


class TimeViewlet(ViewletBase):
    index = ViewPageTemplateFile("time.pt")


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
