from docpool.base.localbehavior.localbehavior import ILocalBehaviorSupport
from docpool.elan.utils import get_scenario_for_current_user
from groupsfolder_setup import GroupsFolderSetupMixin
from playwright.sync_api import expect
from plone import api

import pytest
import transaction


class TestGroupsFolder(GroupsFolderSetupMixin):
    @pytest.fixture(autouse=True)
    def setup(self, acceptance, content_admin_page_factory) -> None:
        self.portal = acceptance["portal"]
        self.page = content_admin_page_factory()
        self.plone_url = self.portal.absolute_url()

        self.docpool = self.portal["bund"]
        self.setup_content()

    def setup_content(self):
        super().setup_content()
        self.groups_folder = self.docpool["content"]["Groups"]["bund_group1"]
        self.subnav = api.content.create(
            container=self.group_folder,
            type="SimpleFolder",
            title="Folder Nav 2",
            description="foo",
            scenario=get_scenario_for_current_user(self.docpool),
        )
        ILocalBehaviorSupport(self.subnav).local_behaviors = ["elan"]
        self.subnav.reindexObject(idxs=["apps_supported"])
        transaction.commit()

    @pytest.mark.flaky(reruns=2)
    def test_group_navigation_second_level(self):
        page = self.page
        page.goto(f"{self.plone_url}/bund/setActiveApp?app=elan")

        groups_root_link = page.get_by_role("link", name="My group folders")
        expect(groups_root_link).to_be_visible()
        groups_root_link.click()
        expect(page).to_have_url(self.group_folder.absolute_url())

        sidebar_nav = page.locator("#portal-column-one .sidebar-groups-tree").first
        current_link = sidebar_nav.locator("a.dp-group-link.current")
        expect(current_link).to_have_count(1)
        expect(current_link).to_have_text("Group1 (Bund)")
        expect(current_link).to_have_attribute("href", self.group_folder.absolute_url())
        second_level_link = sidebar_nav.get_by_role("link", name="Folder Nav 2")
        expect(second_level_link).to_be_visible()
        second_level_link.click()
        expect(page).to_have_url(self.subnav.absolute_url())
        expect(current_link).to_have_count(1)
        expect(current_link).to_have_text("Folder Nav 2")
        expect(current_link).to_have_attribute("href", self.subnav.absolute_url())

    def test_listing_navigation_updates_groups_tree(self):
        page = self.page
        page.goto(f"{self.plone_url}/bund/setActiveApp?app=elan")
        page.goto(self.group_folder.absolute_url())

        desktop_nav = page.locator("#portal-column-one .sidebar-groups-tree").first
        group_link = desktop_nav.locator("a.dp-group-link.current", has_text="Group1 (Bund)")
        expect(group_link).to_have_count(1)

        page.locator("#listing .listing-item").filter(has_text="Folder Nav 2").locator("h3").click()
        expect(page).to_have_url(self.subnav.absolute_url())

        expect(desktop_nav.locator("a.dp-group-link.current", has_text="Folder Nav 2")).to_have_count(1)
        expect(desktop_nav.locator("a.dp-group-link.in-path", has_text="Group1 (Bund)")).to_have_count(1)

        page.go_back()
        expect(page).to_have_url(self.group_folder.absolute_url())
        expect(group_link).to_have_count(1)
