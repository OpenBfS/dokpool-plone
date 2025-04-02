from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

import json


class Listing(BrowserView):
    """Example view called from template"""

    def __call__(self, title=None):
        self.items = json.dumps(("1", "2", "3"))
        return self.index()


class Item(BrowserView):
    """Example view called from template"""

    def __call__(self, title=None):
        self.title = title
        return self.index()
