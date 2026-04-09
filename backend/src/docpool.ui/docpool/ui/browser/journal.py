from docpool.base.config import FOLDER_TYPES
from docpool.base.content.archiving import IArchiving
from docpool.base.content.places import IPlaces
from docpool.base.marker import IJournalContainerMarker
from docpool.base.marker import IJournalEntryMarker
from docpool.elan.utils import get_scenario_for_current_user
from docpool.ui.browser.listing import Listing
from logging import getLogger
from plone import api
from plone.app.textfield.value import RichTextValue
from Products.Five.browser import BrowserView


logger = getLogger(__name__)


class JournalEntries(Listing):
    filters = [
        "journal_title",
        "date",
        "text",
    ]

    def update(self):
        self.query["subcategory"] = ["Journal"]
        self.journal_title = self.request.form.get("journal_title", False)
        journal_folder_uid = self.request.form.get("journal_folder_uid")
        journal_folder = api.content.get(UID=journal_folder_uid) if journal_folder_uid else None
        if journal_folder and (text := self.request.form.get("journalentry-text", "").strip()):
            new = api.content.create(
                container=journal_folder,
                type="DPDocument",
                title=text,
                text=RichTextValue(text, "text/html", "text/x-html-safe"),
                docType="journalentry",
                local_behaviors=["elan"],
                scenario=self.base_query["scenario"],
            )
            logger.info("Created new Journalentry %s", new.absolute_url())


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
            item = self.journals[0]
            url = "{}/@@journalentries?selected_groups={}&amp;journal_title={}&amp;journal_folder_uid={}".format(
                self.context.absolute_url(), item["uid"], item["title"], item["uid"]
            )
            return self.request.response.redirect(url)

        return self.index()
