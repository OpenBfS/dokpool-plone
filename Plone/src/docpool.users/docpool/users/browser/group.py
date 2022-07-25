from docpool.base.utils import possibleDocTypes, possibleDocumentPools
from zope.publisher.browser import BrowserView


class PossibleDocTypes(BrowserView):
    def __call__(self):
        return possibleDocTypes(self.context)


class PossibleDocumentPools(BrowserView):
    def __call__(self):
        return possibleDocumentPools(self.context)
