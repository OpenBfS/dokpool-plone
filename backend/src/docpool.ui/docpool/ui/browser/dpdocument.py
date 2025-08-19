from docpool.base.appregistry import APP_REGISTRY
from Products.Five.browser import BrowserView


class DPDocumentView(BrowserView):
    """View for all DPDocuments."""

    def __call__(self):
        return super().__call__()

    def apps(self):
        results = {}
        for app in APP_REGISTRY:
            if app in self.context.local_behaviors:
                results[app] = self.context.doc_extension(app)
        return results
