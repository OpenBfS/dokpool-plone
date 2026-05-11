from docpool.elan.testing import DOCPOOL_EVENT_FUNCTIONAL_TESTING
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
