from elan.esd.portlets.recent import Renderer
from Products.Five.browser import BrowserView


class RefreshRecent(BrowserView):
    """Return the recent-changes portlets content. Loaded regularly via ajax."""

    def __call__(self):
        rp = Renderer(self.context, self.request, None, None, None)
        self.request.response.setHeader("Cache-Control", "no-cache")
        return rp.render()
