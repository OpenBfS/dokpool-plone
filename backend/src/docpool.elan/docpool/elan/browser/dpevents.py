from docpool.base.content.places import IPlaces
from docpool.elan import DocpoolMessageFactory as _
from docpool.elan.content.dpevents import global_events_folder
from docpool.elan.utils import set_scenario_for_current_user
from docpool.ui.utils import can_view
from plone import api
from Products.Five.browser import BrowserView
from z3c.form import form

import logging


log = logging.getLogger(__name__)


class DPEventsBaseView(BrowserView):
    def __init__(self, context, request):
        super().__init__(context, request)
        self.document_pool = IPlaces(self.context).document_pool

    @property
    def global_events_link(self):
        if self.document_pool is None:
            return
        if can_view(ge := global_events_folder(), "@@view"):
            return ge.absolute_url()


class DPEventsView(DPEventsBaseView):
    """Default view"""

    def number_of_entries(self, dpevent):
        args = {
            "portal_type": "DPDocument",
            "scenario": dpevent.UID(),
        }
        if contentarea := IPlaces(self.context).content:
            args["context"] = contentarea
        return len(api.content.find(**args))

    @property
    def show_edit_link(self):
        return api.user.has_permission("Docpool: Add DPEvent", obj=self.context)


class ManageSubscribedEvents(DPEventsBaseView):
    def __call__(self):
        if self.document_pool is None:
            self.request.response.redirect(self.context.absolute_url())
            return
        self.handle_action()
        return super().__call__()

    def handle_action(self):
        action = self.request.form.get("action")
        sc_uid = self.request.form.get("scenario")
        if not (action or sc_uid):
            return

        if not any(sc_uid == sc.UID() for sc in global_events_folder().getDPEvents()):
            api.portal.show_message(_("Invalid scenario."), self.request, "error")
            return

        if action == "subscribe" and sc_uid not in self.context.subscribed_events:
            self.context.subscribed_events.append(sc_uid)
            api.portal.show_message(_("Scenario subscribed."), self.request)
        elif action == "unsubscribe" and sc_uid in self.context.subscribed_events:
            self.context.subscribed_events.remove(sc_uid)
            api.portal.show_message(_("Scenario unsubscribed."), self.request)
        else:
            api.portal.show_message(_("Invalid action."), self.request, "error")
        self.request.response.redirect(self.request.getURL())

    def get_scenario_actions(self):
        subscribed = set(self.context.subscribed_events)
        return [
            (
                sc,
                "subscribe"
                if sc.UID() not in subscribed
                else "unsubscribe"
                if sc.is_archive_uptodate
                else "archive",
            )
            for sc in sorted(global_events_folder().getDPEvents(), key=lambda sc: sc.UID() not in subscribed)
        ]

    @form.button.buttonAndHandler(_("label_apply", default="Apply"), name="apply")
    def handle_apply(self, action):
        data, errors = self.extractData()
        if "subscribed_events" not in data:
            self.status = _("Error")
            return

        self.context.subscribed_events[:] = data["subscribed_events"]
        self.status = _("Saved")


class SelectScenario(BrowserView):
    def __call__(self):
        set_scenario_for_current_user(self.request.get("scenario"))
        self.request.response.setHeader("Pragma", "no-cache")
        docpool = IPlaces(self.context).document_pool
        return self.request.response.redirect(f"{docpool.absolute_url()}/@@overview")
