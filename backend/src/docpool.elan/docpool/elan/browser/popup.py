from docpool.elan.utils import setCategoriesForCurrentUser
from Products.Five.browser import BrowserView


class SelectCategories(BrowserView):
    """Called by /@@rpopup in esd when filtering chronologie"""

    def __call__(self):
        cats = self.request.get("cats", [])
        setCategoriesForCurrentUser(cats)
        self.request.response.redirect(self.request.get("HTTP_REFERER"))
