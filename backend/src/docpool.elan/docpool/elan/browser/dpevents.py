from docpool.elan.utils import setScenariosForCurrentUser
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class DPEventsView(BrowserView):
    """Default view"""

    __call__ = ViewPageTemplateFile("dpevents.pt")


class EventSelectAction(BrowserView):
    """
    Handles the submit of the EventViewlet
    """

    def __call__(self):
        scnrs = self.request.get("scnrs", [])
        if not scnrs:
            pass
        setScenariosForCurrentUser(scnrs)
        self.request.response.setHeader("Pragma", "no-cache")
        return self.request.response.redirect(self.request.get("HTTP_REFERER", ""))
