from Acquisition import aq_get
from copy import copy
from docpool.base.config import BASE_APP
from docpool.base.config import FOLDER_TYPES
from docpool.base.config import OTHER_TYPES
from docpool.base.config import TRANSFERS_APP
from docpool.base.content.archiving import IArchiving
from docpool.base.content.places import IPlaces
from docpool.elan.config import ELAN_APP
from docpool.elan.utils import get_scenario_for_current_user
from docpool.ui import _
from plone import api
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

    def __call__(self, limit=0):
        uids, modified = self.find(limit)

        # Mod-Date dazu und hash über udis & mod-date
        self.items = uids
        self.is_archive = IArchiving(self.context).is_archive
        self.json_items = json.dumps(uids)
        self.modified = json.dumps(modified.timeTime()) if modified else None
        return self.index()

    def find(self, limit=0):
        form = self.request.form
        self.folder_listing = self.context.portal_type in FOLDER_TYPES

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
            if event := get_scenario_for_current_user():
                self.base_query["scenario"] = event

        # Filter by Category
        self.selected_subcategories = form.get("selected_subcategories") or []
        if self.selected_subcategories:
            self.query["subcategory"] = self.selected_subcategories

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
            startdate = extract_date(form.get("startdate"))
            starttime = extract_time(form.get("starttime"))
            enddate = extract_date(form.get("enddate"))
            endtime = extract_time(form.get("endtime"))
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
                "review_states": ["private"],
            },
            "pending": {
                "title": _("Pending"),
                "review_states": [
                    "pending",
                    "pending_authority",
                    "pending_bfs",
                    "pending_bmu",
                    "pending_second",
                ],
            },
            "published": {
                "title": _("Published"),
                "review_states": ["published"],
            },
            "revised": {
                "title": _("Revised"),
                "review_states": ["revised"],
            },
        }
        self.selected_review_states = form.get("review_states") or []
        if self.selected_review_states:
            filtered_by_review_states = []
            for state in self.selected_review_states:
                filtered_by_review_states.extend(review_state_filter_config[state]["review_states"])
            self.query["review_state"] = filtered_by_review_states

        # Filter by context
        # TODO: Remove implicit default filtering on path + /content in docpool.elan.monkey
        if self.folder_listing:
            content_area = self.context
            self.base_query["path"] = {
                "query": "/".join(content_area.getPhysicalPath()),
                "depth": 1,
            }
        else:
            content_area = IPlaces(self.context).content
            self.base_query["path"] = "/".join((content_area or self.context).getPhysicalPath())

        # Prepare review_state filter options (query needs to be complete)
        if "visibility" in self.filters:
            for state in review_state_filter_config:
                count = self.count_options({
                    "review_state": review_state_filter_config[state]["review_states"]
                })
                review_state_filter_config[state]["count"] = count
            self.review_states = review_state_filter_config

        # Prepare Entrytypes filter options (query needs to be complete)
        # breakpoint()
        self.doctype_categories = self.doctype_options() if "entrytype" in self.filters else []

        # Prepare Group filter options (query needs to be complete)
        self.groups = {}
        # TODO: Check if we need UserFolder in some context
        if "group" in self.filters and content_area:
            group_query = {
                "portal_type": ["DPTransferFolder", "GroupFolder"],
                "unrestricted": True,  # Readers have no access to the group folders.
                "active_apps": self.active_apps,
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

        # Hook to override
        self.update()

        # Merge base query with and manual filters for real results
        query = self.base_query | self.query
        brains = catalog(**query)
        uids = [brain.UID for brain in brains]
        modified = max(brain.modified for brain in brains) if brains else None

        self.count_without_scenario_filter = None
        if not self.bypass_scenario_filter:
            query.pop("scenario", None)
            self.count_without_scenario_filter = len(catalog(**query)) - len(brains)

        if self.limit > 0:
            uids = uids[: self.limit]

        self.folder_uids = []
        self.other_uids = []
        if self.folder_listing:
            if self.context.portal_type == "Groups":
                # Logic stolen from content-area navigation in getFoldersForCurrentUser
                # TODO: Replace or improve when adding folder-navigation
                gtool = api.portal.get_tool("portal_groups")
                folder_query = {
                    "portal_type": "GroupFolder",
                    "sort_on": "getObjPositionInParent",
                }
                for brain in api.content.find(context=self.context, **folder_query):
                    try:
                        grp = gtool.getGroupById(brain.id)
                        etypes = grp.getProperty("allowedDocTypes", [])
                        if etypes:
                            self.folder_uids.append(brain.UID)
                    except Exception:
                        pass
            else:
                # All folders we should show in the listing
                folder_query = {
                    "portal_type": FOLDER_TYPES,
                    "path": query["path"],
                    "sort_on": "getObjPositionInParent",
                    "active_apps": self.active_apps,
                }
                self.folder_uids = [brain.UID for brain in catalog(**folder_query)]

            # Find other content for the listing
            other_query = {
                "portal_type": OTHER_TYPES,
                "path": query["path"],
                "sort_on": "getObjPositionInParent",
                "active_apps": self.active_apps,
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
                    results[brain.category][brain.subcategory] = {"count": count}
        return {k: v for k, v in results.items() if v}

    def update(self):
        # Allow overriding queries
        return


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
