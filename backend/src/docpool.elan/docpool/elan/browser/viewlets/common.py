from AccessControl.SecurityInfo import allow_module
from docpool.base.content.archiving import IArchiving
from docpool.base.content.places import IPlaces
from docpool.elan.config import ELAN_APP
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter


allow_module("docpool.elan.browser")
allow_module("docpool.elan.browser.viewlets")
allow_module("docpool.elan.browser.viewlets.common")


class ELANViewlet(ViewletBase):
    def isSupported(self):
        dp_app_state = getMultiAdapter((self.context, self.request), name="dp_app_state")
        return dp_app_state.isCurrentlyActive(ELAN_APP)

    @property
    def available(self):
        return IPlaces(self.context).document_pool is not None and self.isSupported()


class TickerViewlet(ELANViewlet):
    index = ViewPageTemplateFile("ticker.pt")

    @property
    def available(self):
        return not IArchiving(self.context).is_archive and super().available

    def ticker(self):
        # Contentconfig not not accessible to Reader role but we need to access the ticker
        contentconfig = self.context.unrestrictedTraverse("contentconfig")
        if contentconfig and "ticker" in contentconfig:
            return contentconfig["ticker"]
