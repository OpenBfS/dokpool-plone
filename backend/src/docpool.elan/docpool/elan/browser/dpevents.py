from Acquisition import aq_get
from docpool.elan.utils import set_scenario_for_current_user
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
            "scenario": dpevent.UID(),
        }
        return len(api.content.find(context=contentarea, **args))


class SelectScenario(BrowserView):
    def __call__(self):
        set_scenario_for_current_user(self.request.get("scenario"))
        self.request.response.setHeader("Pragma", "no-cache")
        return self.request.response.redirect(self.request.get("HTTP_REFERER", ""))
