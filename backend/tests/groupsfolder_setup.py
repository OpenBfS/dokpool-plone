from conftest import BUND_CONTENT_ADMIN_NAME
from datetime import datetime
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
        self.entry1 = api.content.create(
            container=self.group_folder,
            type="DPDocument",
            title="Weatherinfo without images",
            description="foo",
            docType="weather_conditions_and_forecast",
            local_behaviors=["elan"],
            scenario=get_scenario_for_current_user(self.docpool),
        )
        self.entry1.creation_date = datetime(2026, 1, 1, 14, 00, 00)
        self.entry1.mdate = datetime(2026, 1, 1, 14, 00, 00)
        self.entry1.reindexObject()
        assert self.entry1.created_by == expected_creator

        # create second entry
        self.entry2 = api.content.create(
            container=self.group_folder,
            type="DPDocument",
            title="Staff Note",
            description="foo",
            docType="staff_note",
            local_behaviors=["elan"],
            scenario=get_scenario_for_current_user(self.docpool),
        )
        self.entry2.creation_date = datetime(2026, 6, 1, 14, 00, 00)
        self.entry2.reindexObject()
        assert self.entry2.created_by == expected_creator
        # add attachments
        filename = os.path.join(os.path.dirname(__file__), "image.png")
        with open(filename, "rb") as f:
            IMAGE_DATA = f.read()
        api.content.create(
            container=self.entry2,
            type="Image",
            title="Some Image",
            description="foo",
            image=NamedBlobImage(data=IMAGE_DATA, filename="image.png"),
        )

        filename = os.path.join(os.path.dirname(__file__), "file.pdf")
        with open(filename, "rb") as f:
            FILE_DATA = f.read()
        api.content.create(
            container=self.entry2,
            type="File",
            title="Some File",
            description="bar",
            file=NamedBlobFile(data=FILE_DATA, filename="file.pdf"),
        )
        self.entry2.mdate = datetime(2026, 6, 1, 14, 00, 00)

        # The review folder supplies the workflow for pending tasks.
        self.review_folder = api.content.create(
            container=self.group_folder2,
            type="ReviewFolder",
            title="Review",
            local_behaviors=["elan"],
        )
        self.entry3 = api.content.create(
            container=self.review_folder,
            type="DPDocument",
            title="Pending review entry",
            docType="staff_note",
            local_behaviors=["elan"],
            scenario=get_scenario_for_current_user(self.docpool),
        )
        api.content.transition(obj=self.entry3, transition="submit")
        self.entry3.creation_date = datetime(2026, 3, 1, 14, 00, 00)
        self.entry3.reindexObject()
        transaction.commit()
