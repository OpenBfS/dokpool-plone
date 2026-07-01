from conftest import BUND_CONTENT_ADMIN_NAME
from docpool.api.browser.setup import add_user
from docpool.base.localbehavior.localbehavior import ILocalBehaviorSupport
from docpool.elan.utils import get_scenario_for_current_user
from plone import api
from plone.app.testing import login
from plone.app.testing import logout
from plone.namedfile.file import NamedBlobFile
from plone.namedfile.file import NamedBlobImage

import os
import transaction


class GroupsFolderSetupMixin:
    def setup_content(self):
        add_user(
            self.docpool,
            BUND_CONTENT_ADMIN_NAME,
            ["group1", "group2"],
            enabled_apps=["elan"],
        )
        content = self.docpool["content"]
        assert content.keys() == ["Transfers", "Members", "Groups"]
        assert BUND_CONTENT_ADMIN_NAME in content["Members"]
        assert BUND_CONTENT_ADMIN_NAME not in self.portal["Members"]

        # assign app to groupfolder to make is show up in navigation (#5434)
        self.group_folder = content["Groups"]["bund_group1"]
        self.group_folder2 = content["Groups"]["bund_group2"]
        ILocalBehaviorSupport(self.group_folder).local_behaviors = ["elan"]
        ILocalBehaviorSupport(self.group_folder2).local_behaviors = ["elan"]
        self.group_folder.reindexObject(idxs=["apps_supported"])
        self.group_folder2.reindexObject(idxs=["apps_supported"])
        logout()
        login(self.portal, BUND_CONTENT_ADMIN_NAME)
        expected_creator = (BUND_CONTENT_ADMIN_NAME, "Content Admin (Bund)", "Group1 (Bund)")

        # create first entry
        self.entry = api.content.create(
            container=self.group_folder,
            type="DPDocument",
            title="Weatherinfo without images",
            description="foo",
            docType="weather_conditions_and_forecast",
            local_behaviors=["elan"],
            scenario=get_scenario_for_current_user(),
        )
        assert self.entry.created_by == expected_creator

        # create second entry
        self.entry = api.content.create(
            container=self.group_folder,
            type="DPDocument",
            title="Staff Note",
            description="foo",
            docType="staff_note",
            local_behaviors=["elan"],
            scenario=get_scenario_for_current_user(),
        )
        assert self.entry.created_by == expected_creator
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
        transaction.commit()
