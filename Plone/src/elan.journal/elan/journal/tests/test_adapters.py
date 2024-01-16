from datetime import datetime
from elan.journal.adapters import IJournalEntryContainer
from elan.journal.adapters import JournalEntry
from elan.journal.testing import INTEGRATION_TESTING
from plone import api

import unittest


class ContentTypeTestCase(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.portal.portal_types["Journal"].global_allow = True
        with api.env.adopt_roles(["Manager"]):
            self.journal = api.content.create(self.portal, "Journal", "journal")

    def test_adding(self):
        adapter = IJournalEntryContainer(self.journal)
        adapter.add(JournalEntry("One", "First journalentry."))
        adapter.add(JournalEntry("Two", "Second journalentry."))
        adapter.add(JournalEntry("Three", "Third journalentry."))
        self.assertEqual(len(adapter), 3)

        # check the first journalentry
        self.assertEqual(adapter[0].creator, "test_user_1_")
        self.assertTrue(isinstance(adapter[0].created, datetime))
        self.assertTrue(isinstance(adapter[0].modified, datetime))
        self.assertEqual(adapter[0].created, adapter[0].modified)
        self.assertEqual(adapter[0].title, "One")
        self.assertEqual(adapter[0].text, "First journalentry.")

        # dates are sequential
        self.assertTrue(adapter[0].created < adapter[1].created)
        self.assertTrue(adapter[1].created < adapter[2].created)

        # check the other journal-entries
        self.assertEqual(adapter[1].title, "Two")
        self.assertEqual(adapter[2].title, "Three")
        self.assertEqual(adapter[1].text, "Second journalentry.")
        self.assertEqual(adapter[2].text, "Third journalentry.")
