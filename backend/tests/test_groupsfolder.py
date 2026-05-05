from docpool.base.localbehavior.localbehavior import ILocalBehaviorSupport
from docpool.elan.utils import get_scenario_for_current_user
from groupsfolder_setup import GroupsFolderSetupMixin
from playwright.sync_api import expect
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME

import pytest
import transaction


class TestGroupsFolder(GroupsFolderSetupMixin):
    @pytest.fixture(autouse=True)
    def setup(self, portal_factory, playwright_page_factory) -> None:
        self.portal = portal_factory(username=TEST_USER_NAME, roles=["Manager"])
        self.page = playwright_page_factory(username=SITE_OWNER_NAME, password=SITE_OWNER_PASSWORD)
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
            scenario=get_scenario_for_current_user(),
        )
        ILocalBehaviorSupport(self.subnav).local_behaviors = ["elan"]
        self.subnav.reindexObject(idxs=["apps_supported"])
        transaction.commit()

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
