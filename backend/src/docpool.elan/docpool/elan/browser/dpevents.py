from docpool.base.content.places import IPlaces
from docpool.elan.utils import set_scenario_for_current_user
from plone import api
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class DPEventsView(BrowserView):
    """Default view"""

    __call__ = ViewPageTemplateFile("dpevents.pt")

    def number_of_entries(self, dpevent):
        args = {
            "portal_type": "DPDocument",
            "scenario": dpevent.UID(),
        }
        if contentarea := IPlaces(self.context).content:
            args["context"] = contentarea
        return len(api.content.find(**args))


class SelectScenario(BrowserView):
    def __call__(self):
        set_scenario_for_current_user(self.request.get("scenario"))
        self.request.response.setHeader("Pragma", "no-cache")
        return self.request.response.redirect(self.request.get("HTTP_REFERER", ""))
