from docpool.api.browser.setup import add_user
from docpool.base.localbehavior.localbehavior import ILocalBehaviorSupport
from docpool.elan.utils import getScenariosForCurrentUser
from docpool.ui.testing import DOCPOOL_UI_FUNCTIONAL_TESTING
from docpool.ui.testing import DOCPOOL_UI_INTEGRATION_TESTING
from plone import api
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.utils import datify
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
            scenarios=getScenariosForCurrentUser(),
        )
        self.assertEqual(self.entry.created_by, ("user1", "user1 (Bund)", "Group1 (Bund)"))
        # add attachments
        filename = os.path.join(os.path.dirname(__file__), "image.png")
        with open(filename, "rb") as f:
            FILE_DATA = f.read()

        api.content.create(
            container=self.entry,
            type="Image",
            title="Some Image",
            description="foo",
            image=NamedBlobImage(data=FILE_DATA, filename="image.png"),
        )
        api.content.create(
            container=self.entry,
            type="Image",
            title="Another Image",
            description="bar",
            image=NamedBlobImage(data=FILE_DATA, filename="image2.png"),
        )

    def test_listing_view_with_entries(self):
        listing_view = api.content.get_view("listing", self.group_folder, self.request)
        # One item is found
        self.assertEqual(listing_view.find(), ([self.entry.UID()], self.entry.modified()))

        # render listing view
        html = listing_view()
        self.assertIn(
            f'<a class="pat-inject list-item-inject-link" data-pat-inject="trigger: autoload-visible; delay: 50; target: self" href="@@listing-item?uid={self.entry.UID()}" >',
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

        # Test data
        data = listing_item_view.dpdocument
        self.assertEqual(data["state_title"], "Private")
        self.assertEqual(data["modified_by_group"], "Group1 (Bund)")
        self.assertEqual(data["modified_by_user"], "user1 (Bund)")
        self.assertEqual(data["available_transitions"][0]["id"], "publish")

        # It needs a valid uid of a DPDocument the user can access
        self.assertIsNone(listing_item_view(uid=self.group_folder.UID()))

    def test_dpdocument_view(self):
        dpdocument_view = api.content.get_view("view", self.entry, self.request)
        self.assertEqual(list(dpdocument_view.apps().keys()), ["elan"])
        html = dpdocument_view()
        self.assertIn("<h1>A Weatherinfo</h1>", html)

    def test_attachments_view(self):
        attachments_view = api.content.get_view("attachments", self.entry, self.request)
        html = attachments_view()
        self.assertIn("(2)", html)
        self.assertIn("zip download", html)

    def test_attachments_list_view(self):
        attachments_list_view = api.content.get_view("attachments_list", self.entry, self.request)
        html = attachments_list_view()
        self.assertIn(f"{self.entry['another-image'].absolute_url()}/@@download", html)

    def test_attachments_grid_view(self):
        attachments_grid_view = api.content.get_view("attachments_grid", self.entry, self.request)
        html = attachments_grid_view()
        self.assertIn(f"{self.entry['another-image'].absolute_url()}/@@download", html)

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
            scenarios=getScenariosForCurrentUser(),
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
