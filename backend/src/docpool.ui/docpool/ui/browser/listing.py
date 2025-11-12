from copy import copy
from docpool.base import DocpoolMessageFactory as _
from docpool.base.behaviors.transferable import ITransferable
from docpool.base.behaviors.utils import allowed_targets
from docpool.base.config import BASE_APP
from docpool.base.config import TRANSFERS_APP
from docpool.base.content.archiving import IArchiving
from docpool.base.content.dpdocument import IDPDocument
from docpool.base.utils import get_current_state_title
from docpool.elan.config import ELAN_APP
from docpool.elan.utils import getScenariosForCurrentUser
from plone import api
from plone.i18n.normalizer.interfaces import IIDNormalizer
from Products.Five.browser import BrowserView
from zope.component import queryUtility

import datetime
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


class Listing(BrowserView):
    """Example view called from template"""

    def __call__(self, limit=0):
        uids, modified = self.find(limit)

        # Mod-Date dazu und hash über udis & mod-date
        self.items = uids
        self.modified = json.dumps(modified.timeTime()) if modified else None
        return self.index()

    def find(self, limit=0):
        form = self.request.form
        self.limit = int(form.get("limit", limit))

        self.selected_doktypes = form.get("selected_doktypes") or []
        self.documenttypes_vocabulary = api.portal.get_vocabulary(
            "docpool.base.vocabularies.DocumentTypes", self.context
        )
        self.selected_review_states = form.get("review_states") or []

        self.query = {
            "context": self.context,
            "portal_type": ["DPDocument"],
            "sort_on": "mdate",
            "sort_order": "reverse",
        }

        # Filter by APP
        dp_app_state = api.content.get_view("dp_app_state", self.context, self.request)
        active_apps = dp_app_state.appsActivatedByCurrentUser()
        active_apps.extend([BASE_APP, TRANSFERS_APP])
        self.query["apps_supported"] = active_apps

        # Filter by DPEvent (ELAN only)
        if ELAN_APP in active_apps and not IArchiving(self.context).is_archive:
            # This filters out archived entries unless the context is in an archive
            if event := getScenariosForCurrentUser():
                self.query["scenarios"] = event

        # Manual filtering
        if self.limit:
            self.query["sort_limit"] = self.limit
        if self.selected_doktypes:
            self.query["dp_type"] = self.selected_doktypes

        # Date filter
        if "form.button.Reset" in form:
            self.startdate = None
            self.starttime = None
            self.enddate = None
            self.endtime = None
        else:
            # Pass original values as string to populate the inputs
            self.startdate = form.get("startdate") or None
            self.starttime = form.get("starttime") or None
            self.enddate = form.get("enddate") or None
            self.endtime = form.get("endtime") or None
            # Transform to use in query
            startdate = extract_date(form.get("startdate"))
            starttime = extract_time(form.get("starttime"))
            enddate = extract_date(form.get("enddate"))
            endtime = extract_time(form.get("endtime"))
            if startdate and starttime:
                startdate = startdate.replace(hour=starttime.hour, minute=starttime.minute)

            if enddate and not endtime:
                enddate = enddate.replace(hour=23, minute=59, second=59)
            elif enddate and endtime:
                enddate = enddate.replace(hour=endtime.hour, minute=endtime.minute, second=59)

            if startdate and enddate:
                self.query["created"] = {
                    "query": (startdate, enddate),
                    "range": "min:max",
                }
            elif startdate:
                self.query["created"] = {
                    "query": startdate,
                    "range": "min",
                }
            elif enddate:
                self.query["created"] = {
                    "query": enddate,
                    "range": "max",
                }

        review_state_filter_config = {
            "private": {
                "title": _("Gruppenintern"),
                "review_states": ["private"],
            },
            "pending": {
                "title": _("Eingereicht"),
                "review_states": [
                    "pending",
                    "pending_authority",
                    "pending_bfs",
                    "pending_bmu",
                    "pending_second",
                ],
            },
            "published": {
                "title": _("Öffentlich"),
                "review_states": ["published"],
            },
            "revised": {
                "title": _("Storniert"),
                "review_states": ["revised"],
            },
        }
        for state in review_state_filter_config:
            count = self.count_options({"review_state": review_state_filter_config[state]["review_states"]})
            review_state_filter_config[state]["count"] = count
        self.review_states = review_state_filter_config

        if self.selected_review_states:
            filtered_by_review_states = []
            for state in self.selected_review_states:
                filtered_by_review_states.extend(review_state_filter_config[state]["review_states"])
            self.query["review_state"] = filtered_by_review_states

        brains = api.content.find(**self.query)
        uids = [brain.UID for brain in brains]
        modified = max(brain.modified for brain in brains) if brains else None

        if self.limit > 0:
            uids = uids[: self.limit]

        return uids, modified

    def count_options(self, extra):
        query = copy(self.query)
        query.update(**extra)
        return len(api.content.find(**query))


def extract_date(value):
    try:
        return datetime.datetime.strptime(value, "%Y-%m-%d")
    except:
        pass


def extract_time(value):
    try:
        return datetime.datetime.strptime(value, "%H:%M")
    except:
        pass


class Item(BrowserView):
    def __call__(self, uid=None):
        obj = api.content.get(UID=uid) if uid else self.context
        if not IDPDocument.providedBy(obj):
            return

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

        icon_name = "question"  # Unknown type
        if docTypeObj := obj.docTypeObj():
            icon_name = docTypeObj.icon_name

        iconresolver = self.context.restrictedTraverse("@@iconresolver")
        attachments = api.content.get_view("contentlisting", obj, self.request)(portal_type=["Image", "File"])

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
            "attachments": attachments,
        }
        return self.index()

    def transition_icon(self, transition_id):
        return TRANSITION_ICON_MAPPING.get(transition_id, "arrow-right")

    def mimetype_name(self, content_type):
        mtr = api.portal.get_tool("mimetypes_registry")
        mimetypes = mtr.lookup(content_type)
        return mimetypes[0].name() if mimetypes else content_type.split("/")[-1]
