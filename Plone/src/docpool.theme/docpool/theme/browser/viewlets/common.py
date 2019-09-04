from AccessControl.SecurityInfo import allow_class
from AccessControl.SecurityInfo import allow_module
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import LogoViewlet

allow_module("elan.esd.browser")
allow_module("elan.esd.browser.viewlets")
allow_module("elan.esd.browser.viewlets.common")


class TimeViewlet(ViewletBase):
    index = ViewPageTemplateFile('time.pt')


allow_class(TimeViewlet)


class LogoDocpoolViewlet(LogoViewlet):

    index = ViewPageTemplateFile('logo.pt')

