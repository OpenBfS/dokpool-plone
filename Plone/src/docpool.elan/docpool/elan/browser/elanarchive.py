from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ELANArchiveView(BrowserView):
    """Default view"""

    __call__ = ViewPageTemplateFile("elanarchive.pt")
