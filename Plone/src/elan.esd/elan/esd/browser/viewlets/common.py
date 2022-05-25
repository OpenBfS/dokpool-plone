from AccessControl.SecurityInfo import allow_module
from docpool.elan.config import ELAN_APP
from plone.app.layout.viewlets.common import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter


allow_module("elan.esd.browser")
allow_module("elan.esd.browser.viewlets")
allow_module("elan.esd.browser.viewlets.common")


class ELANViewlet(ViewletBase):
    def isSupported(self):
        dp_app_state = getMultiAdapter(
            (self.context, self.request), name=u'dp_app_state'
        )
        return dp_app_state.isCurrentlyActive(ELAN_APP)


class TickerViewlet(ELANViewlet):
    index = ViewPageTemplateFile('ticker.pt')

    @property
    def available(self):
        return (
            (not self.context.restrictedTraverse("@@context_helpers").is_archive())
            and self.context.isSituationDisplay()
            and self.isSupported()
        )
