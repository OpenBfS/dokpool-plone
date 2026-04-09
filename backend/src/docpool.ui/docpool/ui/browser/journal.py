from docpool.base.config import FOLDER_TYPES
from docpool.base.content.archiving import IArchiving
from docpool.base.content.places import IPlaces
from docpool.base.marker import IJournalContainerMarker
from docpool.base.marker import IJournalEntryMarker
from docpool.elan.utils import get_scenario_for_current_user
from docpool.ui.browser.listing import Listing
from plone import api
from Products.Five.browser import BrowserView


class JournalEntries(Listing):
    filters = [
        "date",
        "text",
    ]

    def update(self):
        self.query["subcategory"] = ["Journal"]


class Journals(BrowserView):
    def __call__(self):
        # SimpleFolders with id 'journal' that I can see and have 'journalentry' in allowedDocTypes
        self.journals = []
        base_query = {
            "portal_type": "DPDocument",
            "object_provides": IJournalEntryMarker.__identifier__,
            "sort_on": "mdate",
            "sort_order": "descending",
        }
        if not IArchiving(self.context).is_archive:
            if event := get_scenario_for_current_user():
                base_query["scenario"] = event

        query = {
            "portal_type": "SimpleFolder",
            "object_provides": IJournalContainerMarker.__identifier__,
            "sort_on": "path",
        }

        self.folder_listing = self.context.portal_type in FOLDER_TYPES
        if self.folder_listing:
            content_area = self.context
            query["path"] = {
                "query": "/".join(content_area.getPhysicalPath()),
                "depth": 1,
            }
        else:
            content_area = IPlaces(self.context).content
            query["path"] = "/".join((content_area or self.context).getPhysicalPath())

        for brain in api.content.find(**query):
            obj = brain.getObject()
            entries = api.content.find(context=obj, **base_query)
            newest = api.portal.get_localized_time(entries[0].modified, long_format=True) if entries else ""
            data = {
                "count": len(entries),
                "title": obj.title,
                "uid": obj.UID(),
                "group_uid": obj.__parent__.UID(),
                "last_entry": newest,
            }
            self.journals.append(data)

        if len(self.journals) == 1:
            uid = self.journals[0]["group_uid"]
            return self.request.response.redirect(
                f"{self.context.absolute_url()}/@@journalentries?selected_groups={uid}"
            )

        return self.index()
