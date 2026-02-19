from Acquisition import aq_get
from docpool.base.config import BASE_APP
from docpool.base.config import TRANSFERS_APP
from docpool.base.content.archiving import IArchiving
from docpool.base.utils import get_content_area
from docpool.base.utils import getDocumentPoolSite
from docpool.elan.config import ELAN_APP
from docpool.elan.utils import getScenariosForCurrentUser
from plone import api
from Products.Five.browser import BrowserView


class EntryTypes(BrowserView):
    def __call__(self):
        self.items = self.find()
        return self.index()

    def find(self):
        results = {}
        iconresolver = self.context.restrictedTraverse("@@iconresolver")
        catalog = api.portal.get_tool("portal_catalog")

        # Find the right context for the search
        self.is_archive = False
        if IArchiving(self.context).is_archive and getattr(self.context, "myELANArchive", None):
            self.is_archive = True
            self.search_context = self.context.myELANArchive()
        else:
            self.search_context = getDocumentPoolSite(self.context)
        listing_url = f"{self.search_context.absolute_url()}/@@listing"

        # Prepare query-parameters for count_options
        content_area = get_content_area(self.search_context)
        if content_area:
            self.content_area_path = "/".join(content_area.getPhysicalPath())
        else:
            # Is this fallback needed?
            self.content_area_path = "/".join(self.context.getPhysicalPath())

        # Prepare filter by APP
        dp_app_state = api.content.get_view("dp_app_state", self.context, self.request)
        self.active_apps = dp_app_state.appsActivatedByCurrentUser()
        self.active_apps.extend([BASE_APP, TRANSFERS_APP])

        # Filter by DPEvent (ELAN only)
        if not self.is_archive and ELAN_APP in self.active_apps:
            # This filters out archived entries unless the context is in an archive
            if event := getScenariosForCurrentUser():
                self.scenarios = event
        else:
            self.scenarios = None

        # Find categories
        config = aq_get(self.context, "config")
        query = {
            "path": {"query": "/".join(config.getPhysicalPath()), "depth": -1},
            "portal_type": "DocTypeCategory",
            "sort_on": "getObjPositionInParent",
            "apps_supported": self.active_apps,
        }

        for category_brain in api.content.find(**query):
            # Find all subcategories for this category
            subquery = {
                "path": {"query": category_brain.getPath(), "depth": 1},
                "portal_type": "DocTypeSubCategory",
                "sort_on": "getObjPositionInParent",
                "apps_supported": self.active_apps,
            }
            entries = []
            for subcategory_brain in catalog(**subquery):
                # Find all DocTypes for this subcategory
                doctypequery = {
                    "path": {"query": subcategory_brain.getPath(), "depth": 1},
                    "portal_type": ["DocType"],
                    "sort_on": "getObjPositionInParent",
                    "apps_supported": self.active_apps,
                }
                if not catalog(**doctypequery):
                    # Hide subcategories without DocTypes for the current app!
                    continue
                subcategory = subcategory_brain.getObject()
                subcategory_qs = f"selected_subcategories:list={subcategory.title}"
                entry = {
                    "title": subcategory.title,
                    "id": subcategory.id,
                    "listing_url": f"{listing_url}?{subcategory_qs}",
                    "subcategory_icon_url": iconresolver.url(subcategory.icon_name),
                    "count": self.count_options(subcategory.title),
                }
                entries.append(entry)
            if entries:
                results[subcategory.title] = entries

        return results

    def count_options(self, extra):
        query = {
            "portal_type": ["DPDocument"],
            "apps_supported": self.active_apps,
            "path": self.content_area_path,
        }
        if self.scenarios:
            query["scenarios"] = self.scenarios

        # Filter by Subcategory
        query["subcategory"] = extra
        return len(api.content.find(**query))
