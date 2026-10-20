from AccessControl.SecurityInfo import allow_module
from docpool.base.content.places import IPlaces
from docpool.elan.config import ELAN_APP
from plone.app.layout.viewlets.common import ViewletBase
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
