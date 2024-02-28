from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class DocumentPoolView(BrowserView):
    """Default view"""

    __call__ = ViewPageTemplateFile("documentpool.pt")
