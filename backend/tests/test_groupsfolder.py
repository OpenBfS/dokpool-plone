from docpool.base.localbehavior.localbehavior import ILocalBehaviorSupport
from docpool.elan.utils import get_scenario_for_current_user
from groupsfolder_setup import GroupsFolderSetupMixin
from playwright.sync_api import expect
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME

import pytest
import transaction


class TestGroupsFolder(GroupsFolderSetupMixin):
    @pytest.fixture(autouse=True)
    def setup(self, portal_factory, playwright_page_factory) -> None:
        self.portal = portal_factory(username=TEST_USER_NAME, roles=["Manager"])
        self.page = playwright_page_factory()
        self.plone_url = self.portal.absolute_url()

        setRoles(self.portal, TEST_USER_ID, ["Manager"])
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
        expect(page).to_have_url(f"{self.plone_url}/bund/content/Groups")

        sidebar_nav = page.locator(".sidebar-groups-tree")
        second_level_group_link = sidebar_nav.get_by_role("link", name="Group1 (Bund)")
        expect(second_level_group_link).to_be_visible()
        second_level_group_link.click()
        second_level_link = sidebar_nav.get_by_role("link", name="Folder Nav 2")
        expect(second_level_link).to_be_visible()
        second_level_link.click()
        expect(page).to_have_url(f"{self.plone_url}/bund/content/Groups/bund_group1/folder-nav-2")

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
