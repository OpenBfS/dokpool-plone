from docpool.base.utils import extendOptions
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class InfoLinklistitemView(BrowserView):
    """Additional View"""

    __call__ = ViewPageTemplateFile("infolinklistitem.pt")

    def options(self):
        return extendOptions(self.context, self.request, {})
