from Products.Five.browser import BrowserView

import json
import time


class Listing(BrowserView):
    """Example view called from template"""

    def __call__(self, title=None):
        # Do we fetch form catalog? UUIDs?
        self.items = json.dumps(("1", "2", "3"))
        return self.index()


class Item(BrowserView):
    """Example view called from template"""

    def __call__(self, title=None):
        self.title = title
        if title == "1":
            time.sleep(2)
        if title == "2":
            time.sleep(5)
        if title == "3":
            time.sleep(10)
        return self.index()
