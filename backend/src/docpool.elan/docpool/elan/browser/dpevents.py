from docpool.base.content.places import IPlaces
from docpool.elan import DocpoolMessageFactory as _
from docpool.elan.content.dpevents import IDPEvents
from docpool.elan.utils import set_scenario_for_current_user
from plone import api
from plone.autoform.form import AutoExtensibleForm
from plone.dexterity.interfaces import IDexterityEditForm
from plone.z3cform import layout
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from z3c.form import form
from zope.interface import implementer

import logging


log = logging.getLogger(__name__)


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

    @property
    def show_edit_link(self):
        if IPlaces(self.context).document_pool is None:
            return False
        return api.user.has_permission("docpool.elan.AddDPEvent", obj=self.context)


@implementer(IDexterityEditForm)
@layout.wrap_form
class EditSubscribedEvents(AutoExtensibleForm, form.Form):
    label = _("Edit event subscriptions")
    schema = IDPEvents

    def updateActions(self):
        super().updateActions()
        self.actions["apply"].addClass("btn-primary")

    @form.button.buttonAndHandler(_("label_apply", default="Apply"), name="apply")
    def handle_apply(self, action):
        data, errors = self.extractData()
        if "subscribed_events" not in data:
            self.status = _("Error")
            return

        self.context.subscribed_events[:] = data["subscribed_events"]
        self.status = _("Saved")

    @form.button.buttonAndHandler(_("label_cancel", default="Cancel"), name="cancel")
    def handle_cancel(self, action):
        self.request.response.redirect(self.context.absolute_url())


class SelectScenario(BrowserView):
    def __call__(self):
        set_scenario_for_current_user(self.request.get("scenario"))
        self.request.response.setHeader("Pragma", "no-cache")
        return self.request.response.redirect(self.request.get("HTTP_REFERER", ""))
