# -*- coding: utf-8 -*-
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
        pscnrs = self.request.get("pscnrs", [])
        scnrs = self.request.get("scnrs", [])
        scenarios = dict.fromkeys(pscnrs, False)
        scenarios.update(dict.fromkeys(scnrs, True))
        setScenariosForCurrentUser(self.context, scenarios)
        self.context.REQUEST.response.setHeader("Pragma", "no-cache")
        self.context.redirectToReferrerWithParameters("Set filter")
