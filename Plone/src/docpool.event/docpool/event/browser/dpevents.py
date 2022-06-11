from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from docpool.event.utils import setScenariosForCurrentUser


class DPEventsView(BrowserView):
    """Default view
    """

    __call__ = ViewPageTemplateFile('dpevents.pt')


class EventSelectAction(BrowserView):
    """
    Handles the submit of the EventViewlet
    """

    def __call__(self):
        scnrs = self.request.get("scnrs", [])
        if not scnrs:
            pass
        setScenariosForCurrentUser(self.context, scnrs)
        self.context.REQUEST.response.setHeader("Pragma", "no-cache")
        self.context.redirectToReferrerWithParameters("Set filter")
