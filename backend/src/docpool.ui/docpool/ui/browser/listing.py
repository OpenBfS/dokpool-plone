from Acquisition import aq_get
from copy import copy
from docpool.base.config import BASE_APP
from docpool.base.config import FOLDER_TYPES
from docpool.base.config import JOURNALENTRY_ID
from docpool.base.config import OTHER_TYPES
from docpool.base.config import PENDING_STATES
from docpool.base.config import PRIVATE_STATES
from docpool.base.config import PUBLISHED_STATES
from docpool.base.config import REVISED_STATES
from docpool.base.config import TRANSFERS_APP
from docpool.base.content.archiving import IArchiving
from docpool.base.content.places import IPlaces
from docpool.base.marker import IJournalContainerMarker
from docpool.elan.config import ELAN_APP
from docpool.elan.utils import get_scenario_for_current_user
from docpool.ui import _
from docpool.ui.utils import group_has_allowed_document_types
from docpool.ui.utils import is_folder_wizard_context
from plone import api
from plone.protect.authenticator import createToken
from Products.CMFPlone.browser.search import munge_search_term
from Products.Five.browser import BrowserView

import datetime
import json


class Listing(BrowserView):
    """Example view called from template"""

    filters = [
        "entries",
        "date",
        "entrytype",
        "visibility",
        "group",
        "text",
    ]

    features = [
        "sort",
        "print",
        "folder_wizard",
        "entry_wizard",
    ]

    def __call__(self, limit=0):
        form = self.request.form

        # Execute Bulk Actions
        if form.get("uuid"):
            qs = "&".join([f"uid:list={i}" for i in form["uuid"]])
            if "bulk_transfer" in form:
                # redirect to transfer_form
                self.request.response.redirect(f"{self.context.absolute_url()}/dpdocument_transfer_form?{qs}")
            if "bulk_transition" in form:
                # redirect to transition_form
                self.request.response.redirect(
                    f"{self.context.absolute_url()}/@@dpdocument_transition_form?{qs}"
                )
            if "bulk_delete" in form:
                # redirect to delete
                self.request.response.redirect(f"{self.context.absolute_url()}/@@folder_delete?{qs}")
            if "bulk_cut" in form and self.context.portal_type in FOLDER_TYPES:
                # redirect to cut
                self.request.response.redirect(f"{self.context.absolute_url()}/@@folder_cut?{qs}")
        if "bulk_paste" in form and self.context.portal_type in FOLDER_TYPES:
            # redirect to paste
            token = createToken()
            self.request.response.redirect(
                f"{self.context.absolute_url()}/@@folder_paste?_authenticator={token}"
            )

        uids, modified = self.find(limit)

        # Mod-Date dazu und hash über udis & mod-date
        self.items = uids
        self.is_archive = IArchiving(self.context).is_archive
        self.is_journalcontainer = IJournalContainerMarker.providedBy(self.context)
        self.json_items = json.dumps(uids)
        self.modified = json.dumps(modified.timeTime()) if modified else None
        return self.index()

    def find(self, limit=0):
        form = self.request.form
        self.folder_listing = self.context.portal_type in FOLDER_TYPES
        self.folder_wizard_available = is_folder_wizard_context(self.context)

        self.show_bulk_actions = self.folder_listing or self.__name__ in ["tasks"]

        # base_query is the query for results without manual filtering
        self.base_query = {
            "portal_type": ["DPDocument"],
        }
        # query are manual filters
        self.query = {}

        self.limit = int(form.get("limit", limit))

        # Sorting
        self.sort_on_options = {
            "newest": ("mdate", "descending", _("Newest first")),
            "oldest": ("mdate", "ascending", _("Oldest first")),
            "a-z": ("sortable_title", "ascending", _("A-Z")),
            "z-a": ("sortable_title", "descending", _("Z-A")),
        }
        self.sort_on = form.get("sort_on") or "newest"
        sort_on_option = self.sort_on_options.get(self.sort_on) or self.sort_on_options["newest"]
        self.bypass_scenario_filter = form.get("bypass_scenario_filter", False)
        self.query["sort_on"] = sort_on_option[0]
        self.query["sort_order"] = sort_on_option[1]

        self.from_global_search = form.get("from_global_search", False)
        self.global_search_text = form.get("searchable_text", False) or ""
        self.search_scope = form.get("search_scope") or "current_event"
        if self.search_scope == "all_events":
            self.bypass_scenario_filter = True

        # Filter by Text
        self.searchable_text = form.get("searchable_text")
        if self.searchable_text:
            self.query["SearchableText"] = munge_search_term(self.searchable_text)

        # Always filter by APP
        dp_app_state = api.content.get_view("dp_app_state", self.context, self.request)
        self.active_apps = dp_app_state.appsActivatedByCurrentUser()
        self.active_apps.extend([BASE_APP, TRANSFERS_APP])
        self.base_query["apps_supported"] = self.active_apps

        # Filter by DPEvent unless disabled, not in ELAN or in Archive
        if (
            not self.bypass_scenario_filter
            and ELAN_APP in self.active_apps
            and not IArchiving(self.context).is_archive
        ):
            if event := get_scenario_for_current_user(self.context):
                self.base_query["scenario"] = event

        self.show_scenario_filter_switch = False
        if self.folder_listing and ELAN_APP in self.active_apps and self.context.portal_type != "Groups":
            self.show_scenario_filter_switch = True

        # Filter by Category
        self.selected_subcategories = form.get("selected_subcategories") or []
        if self.selected_subcategories:
            self.query["subcategory"] = self.selected_subcategories

        # TODO Hacked - Sync it with filter - needs real data
        selected_dp_types = form.get("dp_type") or []
        if selected_dp_types:
            self.query["dp_type"] = {"query": selected_dp_types, "not": [JOURNALENTRY_ID]}
        elif not selected_dp_types and not self.folder_listing:
            # Hide journalentries unless we are listing a folder (might be a journalfolder)
            self.query["dp_type"] = {"not": [JOURNALENTRY_ID]}

        selected_uids = form.get("UID") or []
        if selected_uids:
            self.query["UID"] = selected_uids

        # Filter by Group
        self.selected_groups = form.get("selected_groups") or []
        if self.selected_groups:
            self.query["group"] = self.selected_groups

        # Filter by Date
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
            startdate = extract_date(self.startdate)
            starttime = extract_time(self.starttime)
            enddate = extract_date(self.enddate)
            endtime = extract_time(self.endtime)
            if startdate and starttime:
                startdate = startdate.replace(hour=starttime.hour, minute=starttime.minute)

            if enddate and not endtime:
                enddate = enddate + datetime.timedelta(days=1)
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

        # Filter by review_state
        review_state_filter_config = {
            "private": {
                "title": _("Internal"),
                "review_states": PRIVATE_STATES,
            },
            "pending": {
                "title": _("Pending"),
                "review_states": PENDING_STATES,
            },
            "published": {
                "title": _("Published"),
                "review_states": PUBLISHED_STATES,
            },
            "revised": {
                "title": _("Revised"),
                "review_states": REVISED_STATES,
            },
        }
        self.selected_review_states = form.get("review_states") or []
        if self.selected_review_states:
            filtered_by_review_states = []
            for state in self.selected_review_states:
                filtered_by_review_states.extend(review_state_filter_config[state]["review_states"])
            self.query["review_state"] = filtered_by_review_states

        # Filter by context
        if self.folder_listing:
            content_area = self.context
            self.base_query["path"] = {
                "query": "/".join(content_area.getPhysicalPath()),
                "depth": 1,
            }
        else:
            content_area = IPlaces(self.context).content
            self.base_query["path"] = "/".join((content_area or self.context).getPhysicalPath())

        # Archive-wide search
        if "from_global_search" in form and self.search_scope == "all_archives":
            self.base_query.pop("scenario", None)
            self.bypass_scenario_filter = True
            dp_archive = IPlaces(self.context).document_pool
            self.base_query["path"] = "/".join(dp_archive.getPhysicalPath()) + "/archive"

        # Hook to override (e.g. used for journals and tasks)
        self.update()

        # Prepare review_state filter options (query needs to be complete)
        if "visibility" in self.filters:
            for state in review_state_filter_config:
                count = self.count_options({
                    "review_state": review_state_filter_config[state]["review_states"]
                })
                review_state_filter_config[state]["count"] = count
            self.review_states = review_state_filter_config

        # Prepare Entrytypes filter options (query needs to be complete)
        self.doctype_categories = self.doctype_options() if "entrytype" in self.filters else []

        # Prepare Group filter options (query needs to be complete)
        self.groups = {}
        # TODO: Check if we need UserFolder in some context
        if "group" in self.filters and content_area:
            group_query = {
                "portal_type": ["DPTransferFolder", "GroupFolder"],
                "unrestricted": True,  # Readers have no access to the group folders.
                "apps_supported": self.active_apps,
                "sort_on": ["portal_type", "sortable_title"],
            }
            for brain in api.content.find(context=content_area, **group_query):
                # Ignore groups that have no content for the base_query
                show_group = self.count_options({"group": brain.UID}, self.base_query)
                if show_group:
                    count = self.count_options({"group": brain.UID})
                    self.groups[brain.UID] = {"title": brain.Title}
                    self.groups[brain.UID]["count"] = count

        catalog = api.portal.get_tool("portal_catalog")

        # Merge base query with and manual filters for real results
        query = self.base_query | self.query
        brains = catalog(**query)
        brains = [brain for brain in brains if self.include_brain(brain)]
        uids = [brain.UID for brain in brains]
        self.total_count = len(uids)
        modified = max(brain.modified for brain in brains) if brains else None

        self.count_without_scenario_filter = None
        if not self.bypass_scenario_filter:
            query.pop("scenario", None)
            self.count_without_scenario_filter = len(catalog(**query)) - len(brains)

        if self.limit > 0:
            uids = uids[: self.limit]

        self.show_global_search_summary = bool(
            self.from_global_search and self.global_search_text and "entries" in self.filters
        )

        self.folder_uids = []
        self.other_uids = []
        if self.folder_listing:
            if self.context.portal_type == "Groups":
                # Logic stolen from content-area navigation in getFoldersForCurrentUser
                # TODO: Replace or improve when adding folder-navigation
                gtool = api.portal.get_tool("portal_groups")
                folder_query = {
                    "portal_type": ["DPTransferFolder", "GroupFolder", "SimpleFolder"],
                    "sort_on": ["portal_type", "sortable_title"],
                    "apps_supported": self.active_apps,
                }
                for brain in api.content.find(context=self.context, depth=1, **folder_query):
                    if group_has_allowed_document_types(brain.id, gtool):
                        self.folder_uids.append(brain.UID)
            else:
                # All folders we should show in the listing
                folder_query = {
                    "portal_type": FOLDER_TYPES,
                    "path": query["path"],
                    "sort_on": "getObjPositionInParent",
                    "apps_supported": self.active_apps,
                }
                self.folder_uids = [brain.UID for brain in catalog(**folder_query)]

            # Find other content for the listing
            other_query = {
                "portal_type": OTHER_TYPES,
                "path": query["path"],
                "sort_on": "getObjPositionInParent",
                "apps_supported": self.active_apps,
            }
            self.other_uids = [brain.UID for brain in catalog(**other_query)]

        return uids, modified

    def reset_url(self, remove=None):
        """Build reset url with some params removed."""
        if not remove:
            return self.request.ACTUAL_URL
        if isinstance(remove, str):
            remove = [remove]
        form = copy(self.request.form)
        for r in remove:
            form.pop(r, None)

        query = []
        for k, v in form.items():
            if isinstance(v, list):
                for item in v:
                    query.append(f"{k}:list={item}")
            else:
                query.append(f"{k}={v}")

        if not query:
            return self.request.ACTUAL_URL

        return f"{self.request.ACTUAL_URL}?{'&'.join(query)}"

    def count_options(self, extra, query=None):
        if not query:
            query = self.query | self.base_query
        else:
            # Do not change the passed query!
            query = copy(query)
        query.update(**extra)
        return len(api.content.find(**query))

    def doctype_options(self):
        """These are DocTypeSubCategories."""
        config = aq_get(self.context, "config", None)
        if not config or config.portal_type != "DPConfig":
            return {}
        query = {
            "portal_type": "DocType",
            "sort_on": "getObjPositionInParent",
            "apps_supported": self.active_apps,
            "getId": {"not": JOURNALENTRY_ID},
        }
        brains = api.content.find(context=config, **query)
        results = {}
        for brain in brains:
            if brain.category not in results:
                results[brain.category] = {}
            if brain.subcategory not in results[brain.category]:
                # Ignore subcategories that have no content for the base_query
                show_subcategory = self.count_options({"subcategory": brain.subcategory}, self.base_query)
                if show_subcategory:
                    count = self.count_options({"subcategory": brain.subcategory})
                    # Get icon parent of obj (which is the subcategory)
                    icon_name = brain.getObject().__parent__.icon_name
                    results[brain.category][brain.subcategory] = {"count": count, "icon_name": icon_name}
        return {k: v for k, v in results.items() if v}

    def update(self):
        # Allow overriding queries
        return

    def include_brain(self, brain):
        # Allow dropping brains from results
        return True


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
