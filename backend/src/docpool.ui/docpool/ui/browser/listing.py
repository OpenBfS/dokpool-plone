from docpool.base.behaviors.transferable import ITransferable
from docpool.base.behaviors.utils import allowed_targets
from docpool.base.utils import get_current_state_title
from docpool.ui.services.newdatacheck.post import Listing as ListingBase
from plone import api
from plone.i18n.normalizer.interfaces import IIDNormalizer
from Products.Five.browser import BrowserView
from zope.component import queryUtility

import json


TRANSITION_ICON_MAPPING = {
    "publish": "eye",
    "reject_second": "box-arrow-in-left",
    "reject_to_authority": "box-arrow-in-left",
    "reject_to_bfs": "box-arrow-in-left",
    "reject_to_npp_operator": "box-arrow-in-left",
    "reject": "box-arrow-in-left",
    "retract_for_revision": "box-arrow-in-left",
    "retract_to_authority": "box-arrow-in-left",
    "retract_to_bfs": "box-arrow-in-left",
    "retract_to_npp_operator": "box-arrow-in-left",
    "retract": "eye-slash",
    "submit_authority": "arrow-right",
    "submit_bfs": "arrow-right",
    "submit_bmu": "arrow-right",
    "submit_second": "arrow-right",
    "submit": "arrow-right",
}

# TODO: Either configure in registry/controlpanel or on doktype
DOCTYPE_ICON_MAPPING = {
    "airactivity": "wind",
    "doksysdok": "file-earmark-text",
    "estimation": "radioactive",
    "eventinformation": "calendar-event",
    "gammadoserate": "radioactive",
    "gammadoserate_mobile": "radioactive",
    "gammadoserate_timeseries": "radioactive",
    "groundcontamination": "radioactive",
    "info_ecc": "info-circle",
    "info_public": "info-circle",
    "information_expert_advisor": "card-checklist",
    "inquiry_measurement_order": "radioactive",
    "instructions": "card-checklist",
    "lasair_lasat_projection": "radioactive",
    "measurement_order": "rulers",
    "measurement_requirements": "rulers",
    "mediarelease": "newspaper",
    "mediareport": "newspaper",
    "mresult_feed": "flask",
    "mresult_flight": "flask",
    "mresult_food": "flask",
    "mresult_insitu": "flask",
    "mresult_other": "flask",
    "mresult_water": "flask",
    "note": "card-text",
    "note_measurement_teams": "flask",
    "notification": "bell",
    "nppinformation": "radioactive",
    "operation_map": "map",
    "other_document": "radioactive",
    "otherprojection": "radioactive",
    "protectiveactions": "radioactive",
    "reireport": "radioactive",
    "rodosprojection": "radioactive",
    "sitrep": "radioactive",
    "situationreport": "radioactive",
    "trajectory": "compass",
    "weatherinformation": "cloud-rain",
}


class Listing(ListingBase, BrowserView):
    """Example view called from template"""

    def __call__(self, limit=0):
        uids, modified = self.find(limit)

        # Mod-Date dazu und hash über udis & mod-date
        self.items = uids
        self.modified = json.dumps(modified.timeTime()) if modified else None
        return self.index()


class Item(BrowserView):
    """Example view called from template"""

    def __call__(self, uid=None):
        obj = api.content.get(UID=uid)

        review_state = api.content.get_state(obj)
        review_state_title = get_current_state_title(obj, review_state)

        idnormalizer = queryUtility(IIDNormalizer)
        state_class = f"state-{idnormalizer.normalize(review_state)}"
        portal_workflow = api.portal.get_tool("portal_workflow")
        available_transitions = portal_workflow.getTransitionsFor(obj)

        if userinfo := obj.modified_by or obj.created_by:
            userinfo = userinfo.replace("<i>", "--separator--<i>", 1)
            modified_by_user = userinfo.split("--separator--")[0].strip()
            modified_by_group = userinfo.split("--separator--")[1] if "--separator--" in userinfo else ""

        show_transfer_action = False
        if api.user.has_permission("Docpool: Send Content", obj=obj):
            try:
                adapted = ITransferable(obj)
            except TypeError:
                pass
            else:
                if adapted.transferable() and allowed_targets(obj):
                    show_transfer_action = True

        icon_name = self.doctype_icon(obj.docType)
        iconresolver = self.context.restrictedTraverse("@@iconresolver")

        self.dpdocument = {
            "date": obj.mdate,
            "title": obj.title,
            "id": obj.id,
            "description": obj.description,
            "review_state": review_state,
            "state_title": review_state_title,
            "state_class": state_class,
            "available_transitions": available_transitions,
            "uid": uid,
            "doctype": obj.docType,
            "doctype_icon_url": iconresolver.url(icon_name),
            "url": obj.absolute_url(),
            "path": obj.absolute_url_path(),
            "modified_by_user": modified_by_user,
            "modified_by_group": modified_by_group,
            "show_transfer_action": show_transfer_action,
        }
        return self.index()

    def transition_icon(self, transition_id):
        return TRANSITION_ICON_MAPPING.get(transition_id, "arrow-right")

    def doctype_icon(self, doctype):
        return DOCTYPE_ICON_MAPPING.get(doctype, "radioactive")
