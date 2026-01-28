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
        dp = getDocumentPoolSite(self.context)
        listing_url = f"{dp.absolute_url()}/@@listing"
        iconresolver = self.context.restrictedTraverse("@@iconresolver")
        catalog = api.portal.get_tool("portal_catalog")

        # Prepare filter by APP
        dp_app_state = api.content.get_view("dp_app_state", self.context, self.request)
        self.active_apps = dp_app_state.appsActivatedByCurrentUser()
        self.active_apps.extend([BASE_APP, TRANSFERS_APP])

        # Collect DokTypes without Catagory (e.g. REI, RODOS)
        # TODO: Remove this if we only allow categorized Doctypes!
        # without_category = []
        # query = {
        #     "path": {"query": "/".join(self.context.getPhysicalPath()), "depth": 1},
        #     "portal_type": ["DocType"],
        #     "sort_on": "getObjPositionInParent",
        #     "apps_supported": self.active_apps,
        # }
        # for brain in catalog(**query):
        #     doctypeobj = brain.getObject()
        #     entry = {
        #         "title": brain.Title,
        #         "id": brain.id,
        #         "url": brain.getURL(),
        #         "listing_url": f"{listing_url}?selected_doctypes:list={brain.id}",
        #         "doctype_icon_url": iconresolver.url(doctypeobj.icon_name),
        #         "count": self.count_options(brain.id),
        #         "can_edit": api.user.has_permission("Modify portal content", obj=doctypeobj),
        #     }
        #     without_category.append(entry)
        # if without_category:
        #     results["Without category"] = without_category

        # Find categories
        query = {
            "path": {"query": "/".join(self.context.getPhysicalPath()), "depth": 1},
            "portal_type": ["DocTypeCategory"],
            "sort_on": "getObjPositionInParent",
            "apps_supported": self.active_apps,
        }

        for category_brain in api.content.find(**query):
            category = category_brain.getObject()
            # Find all subcategories for this category
            subquery = {
                "path": {"query": "/".join(category.getPhysicalPath()), "depth": 1},
                "portal_type": ["DocTypeCategory"],
                "sort_on": "getObjPositionInParent",
                "apps_supported": self.active_apps,
            }
            entries = []
            for brain in catalog(**subquery):
                subcategory = brain.getObject()
                # Find all DocTypes for this subcategory
                doctypequery = {
                    "path": {"query": "/".join(subcategory.getPhysicalPath()), "depth": 1},
                    "portal_type": ["DocType"],
                    "sort_on": "getObjPositionInParent",
                    "apps_supported": self.active_apps,
                }
                doctype_ids = [i.getId for i in catalog(**doctypequery)]
                if not doctype_ids:
                    # Do not show subcategories without DocTypes that fit the current app!
                    continue
                doctype_ids_qs = "&".join([f"selected_doctypes:list={i}" for i in doctype_ids])
                entry = {
                    "title": subcategory.title,
                    "id": subcategory.id,
                    "listing_url": f"{listing_url}?{doctype_ids_qs}",
                    "subcategory_icon_url": iconresolver.url(subcategory.icon_name),
                    "count": self.count_options(doctype_ids),
                }
                entries.append(entry)
            if entries:
                results[category.title] = entries

        return results

    def count_options(self, extra):
        query = {
            "portal_type": ["DPDocument"],
        }

        # Filter by APP
        dp_app_state = api.content.get_view("dp_app_state", self.context, self.request)
        active_apps = dp_app_state.appsActivatedByCurrentUser()
        active_apps.extend([BASE_APP, TRANSFERS_APP])
        query["apps_supported"] = active_apps

        # Filter by DPEvent (ELAN only)
        if ELAN_APP in active_apps and not IArchiving(self.context).is_archive:
            # This filters out archived entries unless the context is in an archive
            if event := getScenariosForCurrentUser():
                query["scenarios"] = event

        # Filter by context
        # TODO: Handle listing in content-area (which is a folder-listing)
        # TODO: Remove implicit default filtering on path + /content in docpool.elan.monkey
        content_area = get_content_area(self.context)
        if content_area:
            query["path"] = "/".join(content_area.getPhysicalPath())
        else:
            query["path"] = "/".join(self.context.getPhysicalPath())

        # Filter by Doctype
        query["dp_type"] = extra

        return len(api.content.find(**query))
