from docpool.api.browser.setup import add_user
from docpool.base.localbehavior.localbehavior import ILocalBehaviorSupport
from docpool.elan.utils import get_scenario_for_current_user
from docpool.elan.utils import set_scenario_for_current_user
from docpool.ui.testing import DOCPOOL_UI_FUNCTIONAL_TESTING
from docpool.ui.testing import DOCPOOL_UI_INTEGRATION_TESTING
from plone import api
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import TEST_USER_ID
from plone.dexterity.utils import datify
from plone.namedfile.file import NamedBlobFile
from plone.namedfile.file import NamedBlobImage

import datetime
import os
import unittest


class TestUI(unittest.TestCase):
    """Test that docpool.ui is properly installed."""

    layer = DOCPOOL_UI_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_listing_find_on_empty_docpool(self):
        listing_view = api.content.get_view("listing", self.portal, self.request)
        # Nothing found - no UIDs and no modified date
        self.assertEqual(listing_view.find(), ([], None))


class TestUIFeatures(unittest.TestCase):
    """Test docpool.ui features."""

    layer = DOCPOOL_UI_FUNCTIONAL_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.docpool = self.portal["bund"]
        self.setup_content()

    def test_docpool_view_redirects_to_overview(self):
        view = api.content.get_view("view", self.docpool, self.request)
        overview_url = f"{self.docpool.absolute_url()}/@@overview"

        self.assertEqual(view(), overview_url)
        self.assertEqual(self.request.response.getStatus(), 302)
        self.assertEqual(self.request.response.getHeader("Location"), overview_url)

    def test_docpool_listing_remains_available(self):
        listing_view = api.content.get_view("listing", self.docpool, self.request)

        self.assertIsNotNone(listing_view)

    def test_overview_tile_listing_url_uses_tile_query(self):
        tile_view = api.content.get_view("overview-public-information", self.docpool, self.request)
        expected_url = (
            f"{self.docpool.absolute_url()}/@@listing"
            "?dp_type:list=response_action"
            "&dp_type:list=response_action_taken"
            "&dp_type:list=information-for_the_public"
        )

        self.assertEqual(tile_view.listing_url(), expected_url)

    def test_overview_tile_without_results_has_no_count_link(self):
        tile_view = api.content.get_view("overview-public-information", self.docpool, self.request)
        html = tile_view()

        self.assertNotIn("overview-tile-count", html)

    def setup_content(self):
        add_user(self.docpool, "user1", ["group1"], enabled_apps=["elan"])
        content = self.docpool["content"]
        self.assertEqual(content.keys(), ["Transfers", "Members", "Groups"])
        self.assertIn("user1", content["Members"])
        self.assertNotIn("user1", self.portal["Members"])

        # assign app to groupfolder to make is show up in navigation (#5434)
        self.group_folder = content["Groups"]["bund_group1"]
        ILocalBehaviorSupport(self.group_folder).local_behaviors = ["elan"]
        self.group_folder.reindexObject(idxs=["apps_supported"])
        logout()
        login(self.portal, "user1")

        # create entry
        self.entry = api.content.create(
            container=self.group_folder,
            type="DPDocument",
            title="A Weatherinfo",
            description="foo",
            docType="weather_conditions_and_forecast",
            local_behaviors=["elan"],
            scenario=get_scenario_for_current_user(self.docpool),
        )
        self.assertEqual(self.entry.created_by, ("user1", "user1 (Bund)", "Group1 (Bund)"))
        # add attachments
        filename = os.path.join(os.path.dirname(__file__), "image.png")
        with open(filename, "rb") as f:
            IMAGE_DATA = f.read()
        api.content.create(
            container=self.entry,
            type="Image",
            title="Some Image",
            description="foo",
            image=NamedBlobImage(data=IMAGE_DATA, filename="image.png"),
        )

        filename = os.path.join(os.path.dirname(__file__), "file.pdf")
        with open(filename, "rb") as f:
            FILE_DATA = f.read()
        api.content.create(
            container=self.entry,
            type="File",
            title="Some File",
            description="bar",
            file=NamedBlobFile(data=FILE_DATA, filename="file.pdf"),
        )

    def test_listing_view_with_entries(self):
        listing_view = api.content.get_view("listing", self.group_folder, self.request)
        # One item is found
        self.assertEqual(listing_view.find(), ([self.entry.UID()], self.entry.modified()))

        # render listing view
        html = listing_view()
        self.assertIn(
            f'<a class="pat-inject list-item-inject-link" data-pat-inject="trigger: autoload-visible; delay: 50; target: self" href="@@listing-item?uid={self.entry.UID()}&amp;show_bulk_actions=1" >',
            html,
        )

    def test_listing_item_view(self):
        uid = self.entry.UID()

        # The view can be used anywhere. On the portal:
        listing_item_view = api.content.get_view("listing-item", self.portal, self.request)
        html = listing_item_view(uid=uid)
        self.assertIn("A Weatherinfo</h3>", html)

        # On itself:
        listing_item_view = api.content.get_view("listing-item", self.entry, self.request)
        html = listing_item_view(uid=uid)
        self.assertIn("A Weatherinfo</h3>", html)

        # On a group-folder:
        listing_item_view = api.content.get_view("listing-item", self.group_folder, self.request)
        html = listing_item_view(uid=uid)
        self.assertIn("A Weatherinfo</h3>", html)
        self.assertIn("pat-inject list-item-link stretched-link", html)
        html = listing_item_view(uid=uid, use_pat_inject=False)
        self.assertNotIn("pat-inject", html)

        # Test data
        data = listing_item_view.dpdocument
        self.assertEqual(data["state_title"], "Private")
        self.assertEqual(data["modified_by_group"], "Group1 (Bund)")
        self.assertEqual(data["modified_by_user"], "user1 (Bund)")
        self.assertEqual(data["available_transitions"][0]["id"], "publish")

        # It works on Folders as well
        html = listing_item_view(uid=self.group_folder.UID())
        self.assertIn("Group1 (Bund)</h3>", html)

    def test_dpdocument_view(self):
        dpdocument_view = api.content.get_view("view", self.entry, self.request)
        html = dpdocument_view()
        self.assertIn(">A Weatherinfo</h1>", html)

    def test_dpdocument_edit_view(self):
        dpdocument_edit_view = api.content.get_view("edit", self.entry, self.request)
        html = dpdocument_edit_view()
        self.assertIn('class="dp-document-header', html)
        self.assertIn(">Edit the document</h1>", html)
        self.assertIn(f'href="{self.entry.absolute_url()}"', html)
        self.assertIn('id="edit-attachments"', html)
        self.assertIn("(2)", html)
        self.assertIn("zip download", html)
        self.assertIn(f"{self.entry['some-file'].absolute_url()}/@@download", html)
        self.assertNotIn('id="attachments_grid"', html)
        self.assertNotIn('id="attachments_list"', html)
        self.assertIn('class="pat-upload docpool-upload d-flex flex-column my-3"', html)
        self.assertIn("docpool-upload__formats", html)
        self.assertIn("showTitle: false;", html)

    def test_attachments_view(self):
        attachments_view = api.content.get_view("attachments", self.entry, self.request)
        html = attachments_view()
        self.assertIn("(2)", html)
        self.assertIn("zip download", html)

    def test_attachments_list_view(self):
        attachments_list_view = api.content.get_view("attachments_list", self.entry, self.request)
        html = attachments_list_view()
        file_url = self.entry["some-file"].absolute_url()
        self.assertIn(f"{file_url}/@@download", html)
        self.assertIn(f"{file_url}/@@pdfjs_file_view", html)
        self.assertIn('class="pat-plone-modal"', html)
        self.assertIn("modalSizeClass: modal-fullscreen", html)

    def test_attachments_grid_view(self):
        attachments_grid_view = api.content.get_view("attachments_grid", self.entry, self.request)
        html = attachments_grid_view()
        self.assertIn(f"{self.entry['some-file'].absolute_url()}/@@preview", html)
        self.assertIn('class="pat-plone-modal"', html)
        self.assertIn("modalSizeClass: modal-fullscreen", html)

    def test_time_filter(self):
        listing_view = api.content.get_view("listing", self.group_folder, self.request)
        uids, _ = listing_view.find()
        self.assertEqual(len(uids), 1)

        # create entry
        entry = api.content.create(
            container=self.group_folder,
            type="DPDocument",
            title="A Weatherinfo",
            description="foo",
            docType="weather_conditions_and_forecast",
            local_behaviors=["elan"],
            scenario=get_scenario_for_current_user(self.docpool),
        )
        uids, _ = listing_view.find()
        self.assertEqual(len(uids), 2)

        self.request.form["startdate"] = (datetime.date.today() - datetime.timedelta(days=3)).isoformat()
        uids, _ = listing_view.find()
        self.assertEqual(len(uids), 2)

        self.request.form["enddate"] = (datetime.date.today() - datetime.timedelta(days=1)).isoformat()
        uids, _ = listing_view.find()
        self.assertEqual(len(uids), 0)

        # change creation-date of entry2
        older_date = datetime.datetime.now() - datetime.timedelta(days=2)
        entry.creation_date = datify(older_date)
        entry.reindexObject()
        uids, _ = listing_view.find()
        self.assertEqual(len(uids), 1)

    def test_search_scopes_with_current_all_events_and_archive_documents(self):
        events_container = self.portal["contentconfig"]["events"]
        scen_container = self.docpool["contentconfig"]["scen"]

        # Event creation/archiving needs manager
        logout()
        login(self.portal, SITE_OWNER_NAME)
        current_event = api.content.create(
            container=events_container,
            type="DPEvent",
            id="current_scope_event",
            title="Current Scope Event",
        )
        current_event.reindexObject()
        all_events_event = api.content.create(
            container=events_container,
            type="DPEvent",
            id="all_events_scope_event",
            title="All Events Scope Event",
        )
        all_events_event.reindexObject()
        archive_event = api.content.create(
            container=events_container,
            type="DPEvent",
            id="archive_scope_event",
            title="Archive Scope Event",
        )
        archive_event.reindexObject()
        scen_container.subscribed_events.extend((
            current_event.UID(),
            all_events_event.UID(),
            archive_event.UID(),
        ))
        logout()
        login(self.portal, "user1")

        current_doc = api.content.create(
            container=self.group_folder,
            type="DPDocument",
            title="Current Scope Document",
            description="scope-current",
            docType="weather_conditions_and_forecast",
            local_behaviors=["elan"],
            scenario=current_event.UID(),
        )
        all_events_doc = api.content.create(
            container=self.group_folder,
            type="DPDocument",
            title="All Events Scope Document",
            description="scope-all-events",
            docType="weather_conditions_and_forecast",
            local_behaviors=["elan"],
            scenario=all_events_event.UID(),
        )
        archive_doc = api.content.create(
            container=self.group_folder,
            type="DPDocument",
            title="Archive Scope Document",
            description="scope-archive",
            docType="weather_conditions_and_forecast",
            local_behaviors=["elan"],
            scenario=archive_event.UID(),
        )

        # Ensure "current_event" scope points to the expected event.
        set_scenario_for_current_user(current_event.UID())

        logout()
        login(self.portal, SITE_OWNER_NAME)
        archive_form = self.docpool.restrictedTraverse("@@archiveAndClose")
        archive_form()
        self.request.form["event"] = archive_event.UID()
        self.request.form["form.button.submit"] = True
        archive_form()
        logout()
        login(self.portal, "user1")

        listing_view = api.content.get_view("listing", self.docpool, self.request)

        self.request.form.clear()
        self.request.form.update(
            search_scope="current_event",
            from_global_search=1,
            searchable_text="scope",
        )
        uids_current, _ = listing_view.find()
        self.assertEqual(set(uids_current), {current_doc.UID()})

        self.request.form.clear()
        self.request.form.update(
            search_scope="all_events",
            from_global_search=1,
            searchable_text="scope",
        )
        uids_all_events, _ = listing_view.find()
        self.assertEqual(set(uids_all_events), {current_doc.UID(), all_events_doc.UID()})

        self.request.form.clear()
        self.request.form.update(
            search_scope="all_archives",
            from_global_search=1,
            searchable_text="scope",
        )
        uids_all_archives, _ = listing_view.find()
        self.assertEqual(set(uids_all_archives), {archive_doc.UID()})
