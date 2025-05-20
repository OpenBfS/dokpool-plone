from Acquisition import aq_get
from docpool.elan.utils import setScenariosForCurrentUser
from plone import api
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class DPEventsView(BrowserView):
    """Default view"""

    __call__ = ViewPageTemplateFile("dpevents.pt")

    def number_of_entries(self, dpevent):
        contentarea = aq_get(self.context, "content")
        args = {
            "portal_type": "DPDocument",
            "scenarios": dpevent.UID(),
        }
        return len(api.content.find(context=contentarea, **args))


class EventSelectAction(BrowserView):
    """
    Handles the submit of the EventViewlet
    """

    def __call__(self):
        pscnrs = self.request.get("pscnrs", [])
        scnrs = self.request.get("scnrs", [])
        setScenariosForCurrentUser({s: (s in scnrs) for s in pscnrs})
        self.request.response.setHeader("Pragma", "no-cache")
        return self.request.response.redirect(self.request.get("HTTP_REFERER", ""))
