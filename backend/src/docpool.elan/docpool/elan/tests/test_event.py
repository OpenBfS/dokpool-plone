from docpool.elan.testing import DOCPOOL_EVENT_FUNCTIONAL_TESTING
from docpool.elan.utils import get_scenarios_for_user
from docpool.elan.utils import set_scenarios_for_user
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.interfaces import IDexterityFTI

import unittest


class TestEvent(unittest.TestCase):
    layer = DOCPOOL_EVENT_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        docpool = self.portal["test_docpool"]
        self.container = docpool["contentconfig"]["scen"]

    def _get_user_scenarios(self):
        test_user = api.user.get(TEST_USER_ID)
        return get_scenarios_for_user(test_user)

    def _set_user_scenarios(self, scenarios):
        test_user = api.user.get(TEST_USER_ID)
        set_scenarios_for_user(test_user, scenarios)

    def test_types_available(self):
        portal_types = api.portal.get_tool("portal_types")
        self.assertTrue(IDexterityFTI.providedBy(portal_types["DPEvent"]))
        self.assertTrue(IDexterityFTI.providedBy(portal_types["DPEvents"]))
        self.assertTrue(IDexterityFTI.providedBy(portal_types["DPNetwork"]))
        self.assertTrue(IDexterityFTI.providedBy(portal_types["DPNuclearPowerStation"]))

    def test_add_event(self):
        event = api.content.create(
            container=self.container,
            type="DPEvent",
            id="test_event",
            title="Test Event",
        )
        self.assertTrue(event.restrictedTraverse("@@view")())
        self.assertTrue(event.restrictedTraverse("@@edit")())

    def test_added_event_is_active_for_users(self):
        event = api.content.create(
            container=self.container,
            type="DPEvent",
            id="test_event",
            title="Test Event",
        )
        scenarios = self._get_user_scenarios()
        self.assertIn(event.UID(), scenarios)

    def test_archived_event_is_moved(self):
        event = api.content.create(
            container=self.container,
            type="DPEvent",
            id="test_event",
            title="Test Event",
        )
        self.assertIn(event.id, self.container)
        archive_form = event.restrictedTraverse("@@archiveAndClose")
        # Render form
        archive_form()
        # Submit form
        self.layer["request"].form["form.button.submit"] = True
        archive_form()
        self.assertNotIn(event.id, self.container)
        archived_event = api.content.get(UID=event.UID())
        self.assertEqual(archived_event.__parent__.portal_type, "ELANArchive")
        self.assertEqual(archived_event.Status, "closed")
        self.assertEqual(
            archived_event.keys(), ["journal1", "journal2", "journal3", "journal4"]
        )

    def test_archived_event_is_not_active_for_users(self):
        event = api.content.create(
            container=self.container,
            type="DPEvent",
            id="test_event",
            title="Test Event",
        )
        event_uid = event.UID()
        scenarios = self._get_user_scenarios()
        self.assertIn(event_uid, scenarios)
        archive_form = event.restrictedTraverse("@@archiveAndClose")
        self.layer["request"].form["form.button.submit"] = True
        archive_form()
        scenarios = self._get_user_scenarios()
        self.assertNotIn(event_uid, scenarios)

    def test_removed_event_is_not_active_for_users(self):
        event = api.content.create(
            container=self.container,
            type="DPEvent",
            id="test_event",
            title="Test Event",
        )
        event_uid = event.UID()
        scenarios = self._get_user_scenarios()
        self.assertIn(event_uid, scenarios)
        api.content.delete(event)
        scenarios = self._get_user_scenarios()
        self.assertNotIn(event_uid, scenarios)

    def test_added_event_can_be_deactivated_by_user(self):
        event = api.content.create(
            container=self.container,
            type="DPEvent",
            id="test_event",
            title="Test Event",
        )
        event_uid = event.UID()
        scenarios = self._get_user_scenarios()
        self.assertIn(event_uid, scenarios)
        self._set_user_scenarios({event_uid: False})
        scenarios = self._get_user_scenarios()
        self.assertNotIn(event_uid, scenarios)

    def test_added_and_activated_event_is_listed_only_once(self):
        event = api.content.create(
            container=self.container,
            type="DPEvent",
            id="test_event",
            title="Test Event",
        )
        event_uid = event.UID()
        self.assertEqual(1, self._get_user_scenarios().count(event_uid))
        self._set_user_scenarios({event_uid: True})
        self.assertEqual(1, self._get_user_scenarios().count(event_uid))

    def test_removal_keeps_working_for_arbitrary_dpevents(self):
        event = api.content.create(
            container=self.container,
            type="DPEvent",
            id="test_event",
            title="Test Event",
        )
        try:
            api.content.delete(event)
        except Exception as e:
            self.fail(str(e))

    def test_removal_prevented_for_routinemode_dpevent(self):
        event = self.container["routinemode"]
        with self.assertRaises(RuntimeError):
            api.content.delete(event)

    def test_journals_for_event(self):
        event = api.content.create(
            container=self.container,
            type="DPEvent",
            id="test_event",
            title="Test Event",
        )
        # check that 4 journals were added
        self.assertEqual(event.keys(), ["journal1", "journal2", "journal3", "journal4"])
        self.assertEqual(
            [i.title for i in event.contentValues()],
            [
                "Einsatztagebuch BfS",
                "Einsatztagebuch RLZ",
                "Einsatztagebuch SSK",
                "Einsatztagebuch Messdienste",
            ],
        )

        # check the local roles for each journal
        self.assertEqual(
            event.journal1.get_local_roles(),
            (
                ("test_docpool_Journal1_Editors", ("JournalEditor",)),
                ("test_docpool_Journal1_Readers", ("JournalReader",)),
                ("test_user_1_", ("Owner",)),
            ),
        )
        self.assertEqual(
            event.journal2.get_local_roles(),
            (
                ("test_docpool_Journal2_Editors", ("JournalEditor",)),
                ("test_docpool_Journal2_Readers", ("JournalReader",)),
                ("test_user_1_", ("Owner",)),
            ),
        )
        self.assertEqual(
            event.journal3.get_local_roles(),
            (
                ("test_docpool_Journal3_Editors", ("JournalEditor",)),
                ("test_docpool_Journal3_Readers", ("JournalReader",)),
                ("test_user_1_", ("Owner",)),
            ),
        )
        self.assertEqual(
            event.journal4.get_local_roles(),
            (
                ("test_docpool_Journal4_Editors", ("JournalEditor",)),
                ("test_docpool_Journal4_Readers", ("JournalReader",)),
                ("test_user_1_", ("Owner",)),
            ),
        )

        # Check that 2 groups each for up to 5 journals actually exist
        self.assertTrue(api.group.get("test_docpool_Journal1_Readers"))
        self.assertTrue(api.group.get("test_docpool_Journal2_Readers"))
        self.assertTrue(api.group.get("test_docpool_Journal3_Readers"))
        self.assertTrue(api.group.get("test_docpool_Journal4_Readers"))
        self.assertTrue(api.group.get("test_docpool_Journal5_Readers"))
        self.assertIsNone(api.group.get("test_docpool_Journal6_Readers"))

        self.assertTrue(api.group.get("test_docpool_Journal1_Editors"))
        self.assertTrue(api.group.get("test_docpool_Journal2_Editors"))
        self.assertTrue(api.group.get("test_docpool_Journal3_Editors"))
        self.assertTrue(api.group.get("test_docpool_Journal4_Editors"))
        self.assertTrue(api.group.get("test_docpool_Journal5_Editors"))
        self.assertIsNone(api.group.get("test_docpool_Journal6_Editors"))

        # check that permissions are as defined in dp_journal_workflow
        self.assertEqual(
            event.journal1._View_Permission,
            (
                "Manager",
                "ContentAdmin",
                "Site Administrator",
                "DocPoolAdmin",
                "JournalEditor",
                "JournalReader",
            ),
        )
        self.assertEqual(
            event.journal1._Modify_portal_content_Permission,
            (
                "Manager",
                "ContentAdmin",
                "Site Administrator",
                "DocPoolAdmin",
                "JournalEditor",
            ),
        )
