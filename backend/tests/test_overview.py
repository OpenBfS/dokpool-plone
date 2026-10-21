from groupsfolder_setup import GroupsFolderSetupMixin
from playwright.sync_api import expect

import pytest
import transaction


class TestOverview(GroupsFolderSetupMixin):
    @pytest.fixture(autouse=True)
    def setup(self, acceptance, content_admin_page_factory) -> None:
        self.portal = acceptance["portal"]
        self.docpool = self.portal["bund"]
        self.setup_content()
        self.page = content_admin_page_factory()

    def test_situation_report_assignment(self):
        self.assert_category_assignment("radiological_situation_report", "overview_tile_latest_situation")

    def test_notification_assignment(self):
        self.assert_category_assignment("official_notification", "overview_tile_notifications")

    def test_empty_tiles(self):
        self.assert_category_assignment("weather_conditions_and_forecast", None)

    def assert_category_assignment(self, doc_type, expected_tile):
        self.entry1.docType = doc_type
        self.entry1.reindexObject()
        transaction.commit()

        docpool_url = self.docpool.absolute_url()
        self.page.goto(f"{docpool_url}/setActiveApp?app=elan")
        self.page.goto(f"{docpool_url}/@@overview")

        for tile_id in (
            "overview_tile_latest_situation",
            "overview_tile_notifications",
            "overview_tile_public_information",
            "overview_tile_measurements",
        ):
            tile = self.page.locator(f"#{tile_id}")
            expect(tile).to_have_count(1)
            document = tile.get_by_role("heading", name=self.entry1.title, exact=True)
            expect(document).to_have_count(1 if tile_id == expected_tile else 0)
            expect(tile.locator(".listing-item")).to_have_count(1 if tile_id == expected_tile else 0)
