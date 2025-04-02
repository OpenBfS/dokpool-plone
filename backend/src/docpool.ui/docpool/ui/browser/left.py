from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class Left(BrowserView):
    """Example view called from template"""

    index = ViewPageTemplateFile("templates/left.pt")

    def __call__(self, foo=None):
        if foo is not None:
            self.foo = foo
        return self.index()
