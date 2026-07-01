from groupsfolder_setup import GroupsFolderSetupMixin
from pathlib import Path
from playwright.sync_api import expect
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME

import pytest
import re
import transaction


class TestListing(GroupsFolderSetupMixin):
    @pytest.fixture(autouse=True)
    def setup(self, portal_factory, playwright_page_factory) -> None:
        self.portal = portal_factory(username=TEST_USER_NAME, roles=["Manager"])
        self.page = playwright_page_factory()
        self.plone_url = self.portal.absolute_url()

        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.docpool = self.portal["bund"]
        self.setup_content()

    def test_for_viewlet_errors(self):
        page = self.page
        page.goto(f"{self.plone_url}")
        expect(page.locator("body")).not_to_contain_text("error while rendering")

    # Opens dropdown actions and clicks publish
    def test_dropdown_publish_dpdocument(self):
        page = self.page
        page.goto(f"{self.plone_url}/bund/setActiveApp?app=elan")
        page.goto(f"{self.plone_url}/bund/listing")
        # Wait for items to get loaded
        items = page.locator("#listing .listing-item")
        expect(items).to_have_count(2)
        # Tests if the DPDocument (without images) exists
        dp_without_images = page.locator("#listing .listing-item", has_text="Weatherinfo without images")
        expect(dp_without_images).to_have_count(1)
        # Publish the DPDocument
        dp_without_images.get_by_role("button").click()
        dp_without_images.locator("#workflow-transition-publish").click()
        status_msg = page.locator(".statusmessage-info").first
        screenshot_dir = Path("screenshots")
        screenshot_dir.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(screenshot_dir / "acceptance-test-screenshot.png"), full_page=True)
        expect(status_msg).to_contain_text(
            " Info: New review state for Weatherinfo without images: Published"
        )

    def test_dropdown_edit(self):
        page = self.page
        page.goto(f"{self.plone_url}/bund/setActiveApp?app=elan")
        page.goto(f"{self.plone_url}/bund/listing")
        # Wait for items to get loaded
        items = page.locator("#listing .listing-item")
        expect(items).to_have_count(2)
        # Tests if the DPDocument (without images) exists
        dp_without_images = page.locator("#listing .listing-item", has_text="Weatherinfo without images")
        dp_without_images.get_by_role("button").click()
        page.locator(".dropdown").get_by_role("link", name="Edit", exact=True).click()
        page.get_by_role("textbox", name="Title •").click()
        page.locator("#form-widgets-IDublinCore-title").fill("A Weatherinfo with updated title")
        page.locator("iframe").content_frame.get_by_label("Rich Text Area").click()
        page.locator("iframe").content_frame.get_by_label("Rich Text Area").fill("Test text")
        # Click somewhere else, so Save button gets activated
        page.locator("#form-widgets-IDublinCore-title").click()
        page.get_by_role("button", name="Save").click()
        dp_without_images = page.locator(
            "#listing .listing-item", has_text="A Weatherinfo with updated title"
        )
        expect(dp_without_images).to_have_count(1)

    def test_dropdown_delete(self):
        page = self.page
        page.goto(f"{self.plone_url}/bund/setActiveApp?app=elan")
        page.goto(f"{self.plone_url}/bund/listing")
        # Wait for items to get loaded
        items = page.locator("#listing .listing-item")
        expect(items).to_have_count(2)
        # Tests if the DPDocument (without images) exists
        dp_without_images = page.locator("#listing .listing-item", has_text="Weatherinfo without images")
        dp_without_images.get_by_role("button").click()
        page.locator(".dropdown").get_by_role("link", name="Delete", exact=True).click()
        page.get_by_role("button", name="Delete").click()
        # Wait for items to get loaded
        items = page.locator("#listing .listing-item")
        expect(items).to_have_count(1)

    def test_inject_and_go_back(self):
        page = self.page
        page.goto(f"{self.plone_url}/bund/setActiveApp?app=elan")
        page.goto(f"{self.plone_url}/bund/listing")
        # Sort by a-z to prevent issues with same mdate
        page.get_by_role("button", name="Sorting").click()
        page.get_by_role("radio", name="A-Z").click()
        # Open item through pat-inject and the stretched link
        page.locator("#listing .listing-item").first.click()
        # Wait for item actions to get injected
        page.wait_for_selector(".actions .list-group")
        expect(page.locator(".actions .list-group")).to_have_count(1)
        # Go back to listing
        page.get_by_role("link", name="Back").click()
        # Wait for items to get loaded
        items = page.locator("#listing .listing-item")
        expect(items).to_have_count(2)

    def test_listing_filter_category(self):
        page = self.page
        page.goto(f"{self.plone_url}/bund/setActiveApp?app=elan")
        page.goto(f"{self.plone_url}/bund/listing")
        # Filter by catagory
        expect(page.locator("#listing .listing-item")).to_have_count(2)
        page.get_by_role("button", name="Entrytype").click()
        expect(
            page.locator("label").filter(has_text="Wetterlage und -prognosen").locator("span.badge").first
        ).to_contain_text("1")
        expect(
            page.locator("label").filter(has_text="Mitteilungen der Stäbe").locator("span.badge").first
        ).to_contain_text("1")
        page.get_by_role("checkbox", name="Wetterlage und -prognosen").click()
        page.get_by_role("button", name="Filter").click()
        expect(page.locator(".listing-item")).to_have_count(1)

    def test_listing_next_item(self):
        page = self.page
        page.goto(f"{self.plone_url}/bund/setActiveApp?app=elan")
        page.goto(f"{self.plone_url}/bund/listing")
        # Open the first item through pat-inject and the stretched link
        items = page.locator("#listing .list-item-inject-link")
        expect(items).to_have_count(2)
        # Save the two hrefs (@@listing-item?uid=16fe85e237ab46d3a10b8929e2f956be)
        hrefs = items.evaluate_all("els => els.map(e => e.getAttribute('href'))")
        # Extract the uid from the href
        uids = [re.search(r"uid=([0-9a-f]+)", h).group(1) for h in hrefs if h]
        assert len(uids) == 2
        # Click one item
        uid_to_open = uids[0]
        page.locator(f'#listing a.list-item-inject-link[href*="uid={uid_to_open}"] h3').click()
        page.wait_for_selector("a.next-item", state="visible")
        expected_next_uid = uids[1]
        # Check if the correct item is open
        nav = page.locator("ul.list-group[data-current-item]")
        expect(nav).to_have_attribute("data-current-item", uid_to_open)
        # Check if the next item has the other uid
        next_link = page.locator("a.next-item")
        href = next_link.get_attribute("href")
        assert href is not None
        assert f"/resolveuid/{expected_next_uid}" in href

    def test_wizard(self):
        page = self.page
        page.goto(f"{self.plone_url}/bund/setActiveApp?app=elan")
        page.goto(f"{self.plone_url}/bund/@@dpdocument_wizard_1")
        page.locator("#container_uid").select_option(self.group_folder.UID())
        page.locator("input#official_notification").click()
        page.get_by_role("button", name="Next").click()
        page.locator("#form-widgets-IDublinCore-title").fill("Example Entry")
        page.locator("iframe").content_frame.get_by_label("Rich Text Area").click()
        page.locator("iframe").content_frame.get_by_label("Rich Text Area").fill("Test text")
        page.set_input_files("#attachments", ["tests/image.png", "tests/file.pdf"])
        page.get_by_role("button", name="Next").click()

        expect(page.get_by_role("radio", name="Normalfall")).to_be_checked()
        expect(page.get_by_title("Internal")).to_be_checked()
        expect(page.get_by_title("Published")).not_to_be_checked()
        page.get_by_title("Published").click()
        page.get_by_role("button", name="Save").click()

        assert page.url.endswith("/bund")
        expect(page.get_by_text("Created Offizielle Meldung 'Example Entry'")).to_be_visible()

        page.goto(f"{self.plone_url}/bund/content/Groups/bund_group1/example-entry")
        expect(page.locator("h1")).to_have_text("Example Entry", timeout=10000)
        # Check that the image was uploaded
        expect(page.get_by_text("image.png")).to_be_visible()
        # Switch to list and assert content
        page.locator("#attachments_list").click()
        expect(page.get_by_role("cell", name="image.png PNG image 1.2 KB")).to_be_visible()
        expect(page.locator(".field", has_text="Normalfall")).to_be_visible()
        expect(page.locator("#content")).to_contain_text("Test text")
        page.goto(f"{self.plone_url}/bund")
        # Wait for items to get loaded
        page.wait_for_selector("#listing .listing-item", state="visible")
        items = page.locator("#listing .listing-item")
        expect(items).to_have_count(3)
        expect(page.get_by_text("Example Entry")).to_be_visible()
        # Sync to check in Plone
        transaction.commit()
        assert api.content.get_state(self.group_folder["example-entry"]) == "published"

    def test_filter_reset(self):
        page = self.page
        page.goto(f"{self.plone_url}/bund/setActiveApp?app=elan")
        page.goto(f"{self.plone_url}/bund/listing")
        # 1. Prüfen, dass beide Items da sind
        expect(page.locator("#listing .listing-item")).to_have_count(2)
        # 2. Filter öffnen (z.B. Entrytype)
        page.get_by_role("button", name="Entrytype").click()
        # 3. Einen Filter auswählen
        page.get_by_role("checkbox", name="Wetterlage und -prognosen").click()
        page.get_by_role("button", name="Filter").click()
        # 4. Ergebnis prüfen
        expect(page.locator(".listing-item")).to_have_count(1)
        expect(page.get_by_text("Weatherinfo")).to_be_visible()
        expect(page.get_by_text("Staff Note")).not_to_be_visible()
        # 5. Filter nochmal öffnen
        page.get_by_role("button", name="Entrytype").click()
        # 6. Reset durchführen
        reset_button = page.get_by_role("link", name="Reset")
        reset_button.click()
        # 7. Prüfen, dass wieder beide Items da sind
        expect(page.locator("#listing .listing-item")).to_have_count(2)
        expect(page.get_by_text("Weatherinfo")).to_be_visible()
        expect(page.get_by_text("Staff Note")).to_be_visible()

    def test_filter_reset_icon_desktop(self):
        page = self.page
        page.goto(f"{self.plone_url}/bund/setActiveApp?app=elan")
        page.goto(f"{self.plone_url}/bund/listing")

        expect(page.locator("#listing .listing-item")).to_have_count(2)
        page.get_by_role("button", name="Entrytype").click()
        page.get_by_role("checkbox", name="Wetterlage und -prognosen").click()
        page.get_by_role("button", name="Filter").click()

        expect(page.locator(".listing-item")).to_have_count(1)
        assert "selected_subcategories" in page.url

        reset_icon = page.get_by_role("button", name="Entrytype").locator(".dp-filter-reset-icon")
        expect(reset_icon).to_be_visible()
        reset_icon.click()

        expect(page.locator("#listing .listing-item")).to_have_count(2)
        expect(page.get_by_text("Weatherinfo")).to_be_visible()
        expect(page.get_by_text("Staff Note")).to_be_visible()
        assert "selected_subcategories" not in page.url

    def test_filter_reset_mobile(self):
        page = self.page
        # Set viewport to mobile size
        page.set_viewport_size({"width": 375, "height": 667})
        page.goto(f"{self.plone_url}/bund/setActiveApp?app=elan")
        page.goto(f"{self.plone_url}/bund/listing")

        expect(page.locator("#listing .listing-item")).to_have_count(2)

        # Mobile Filter öffnen
        page.locator("#listingMobileFiltersToggle").click()

        # Sektion "Eintragsart" öffnen
        page.locator("#mobile-listing-tab-entrytype").click()
        page.get_by_role("checkbox", name="Wetterlage und -prognosen").check()
        page.locator("#mobile-listing-pane-entrytype button[type='submit']").click()

        # Ergebnis prüfen
        expect(page.locator(".listing-item")).to_have_count(1)
        expect(page.get_by_text("Weatherinfo")).to_be_visible()
        expect(page.get_by_text("Staff Note")).not_to_be_visible()

        # Reset durchführen
        page.locator("#listingMobileFiltersToggle").click()
        page.locator("#mobile-listing-tab-entrytype").click()
        section_reset_button = page.locator(
            "#mobile-listing-pane-entrytype a.btn-secondary", has_text="Reset"
        )
        expect(section_reset_button).to_be_visible()
        href = section_reset_button.get_attribute("href")
        # Es sollte kein selected_subcategories mehr enthalten sein
        assert "selected_subcategories" not in href
        section_reset_button.click()

        # Prüfen, dass wieder beide Items da sind
        expect(page.locator("#listing .listing-item")).to_have_count(2)
        expect(page.get_by_text("Weatherinfo")).to_be_visible()
        expect(page.get_by_text("Staff Note")).to_be_visible()
