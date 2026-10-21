from docpool.base.marker import IJournalContainerMarker
from docpool.base.marker import IJournalEntryMarker
from playwright.sync_api import expect
from utils import fill_rich_text_widget

import pytest
import transaction


class TestJournal:
    @pytest.fixture(autouse=True)
    def setup(self, acceptance, site_owner_page_factory) -> None:
        self.portal = acceptance["portal"]
        self.page = site_owner_page_factory()
        self.plone_url = self.portal.absolute_url()

        self.docpool = self.portal["bund"]
        self.setup_content()

    def setup_content(self):
        # Create a group in bund that can add journalentries
        page = self.page
        page.goto(self.plone_url)
        page.locator("button").filter(has_text="Docpools").click()
        page.get_by_role("link", name="ELAN").click()
        expect(page.locator("#listing-filters")).to_contain_text("0 Entries")

        page.get_by_role("link", name="admin").click()
        page.get_by_role("link", name="User Management", exact=True).click()
        assert page.url.endswith("/bund/@@usergroup-userprefs")
        page.get_by_role("link", name="Groups").click()
        page.get_by_role("link", name="Add New Group").click()
        page.get_by_role("textbox", name="Name •").fill("group1")
        page.get_by_role("textbox", name="Title").fill("Group 1")
        page.locator("#allowedDocTypes-from").select_option([
            "official_notification",
            "radiological_situation_report",
            "journalentry",
        ])
        page.get_by_role("button", name="→").click()
        page.get_by_role("button", name="Save").click()

        transaction.commit()
        self.group_folder = self.docpool["content"]["Groups"]["bund_group1"]
        self.journal_folder = self.group_folder["journal"]
        assert IJournalContainerMarker.providedBy(self.journal_folder)
        assert self.journal_folder.portal_type == "SimpleFolder"
        assert "journalentry" in self.journal_folder.allowedDocTypes
        assert "journalentry" not in self.group_folder.allowedDocTypes
        assert "official_notification" in self.group_folder.allowedDocTypes

        # Add test_user_1_ to that group
        page.goto(f"{self.plone_url}/@@user-information?userid=test_user_1_")
        page.get_by_label("DocPool", exact=True).select_option(self.docpool.UID())
        page.get_by_role("button", name="Save").click()
        page.get_by_role("link", name="Group Memberships").click()
        assert page.url.endswith("plone/@@usergroup-usermembership?userid=test_user_1_")
        page.get_by_role("row", name="Group 1").get_by_role("checkbox").check()
        page.get_by_role("button", name="Add user to selected groups").click()

        page.goto(f"{self.plone_url}/bund")

    @pytest.mark.flaky(reruns=2)
    def test_one_journal(self):
        page = self.page
        page.goto(f"{self.plone_url}/bund/@@journals")
        items = page.locator(".journals .listing-item")
        expect(items).to_have_count(1)
        page.get_by_role("link", name="Protokoll Group 1").click()

        # We see the journal
        url = f"/bund/@@journalentries?selected_groups={self.group_folder.UID()}&journal_title=Protokoll%20Group%201&journal_folder_uid={self.journal_folder.UID()}"
        assert page.url.endswith(url)
        items = page.get_by_role("link", name="Stretched link to details view", exact=True)
        expect(items).to_have_count(0)

        fill_rich_text_widget(page, "Ein neuer Protokolleintrag", editor_id="journalentry-text")
        page.get_by_role("button", name="Add journal entry").click()
        inject_links = page.locator("#listing .list-item-inject-link")
        expect(inject_links).to_have_count(1)
        # Inject happens if visible
        inject_links.first.scroll_into_view_if_needed()
        items = page.get_by_role("link", name="Stretched link to details view", exact=True)
        expect(items).to_have_count(1, timeout=15_000)
        expect(page.locator("#listing .listing-item")).to_have_count(1)

        # Make sure the journalentry is not in @@listing
        page.goto(f"{self.plone_url}/bund/@@listing")
        inject_links = page.locator("#listing .list-item-inject-link")
        expect(inject_links).to_have_count(0)

        transaction.commit()
        assert self.journal_folder.keys() == [".wf_policy_config", "ein-neuer-protokolleintrag"]
        assert self.journal_folder[".wf_policy_config"].workflow_policy_in == "dp-private-folder"
        assert self.journal_folder[".wf_policy_config"].workflow_policy_below == "dp-private-folder"
        entry = self.journal_folder["ein-neuer-protokolleintrag"]
        assert entry.portal_type == "DPDocument"
        assert entry.title == "Ein neuer Protokolleintrag"
        assert entry.text.raw == "<p>Ein neuer Protokolleintrag</p>"
        assert IJournalEntryMarker.providedBy(entry)

        # Make sure the journalentry is not in @@listing
        listing_view = self.docpool.restrictedTraverse("@@listing")
        assert listing_view.find() == ([], None)
