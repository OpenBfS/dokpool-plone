# -*- coding: utf-8 -*-
from datetime import datetime
from elan.journal.adapters import IJournalEntryContainer
from elan.journal.adapters import JournalEntry
from elan.journal.testing import INTEGRATION_TESTING
from plone import api

import unittest


class ContentTypeTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        with api.env.adopt_roles(['Manager']):
            self.journal = api.content.create(self.portal, 'Journal', 'journal')

    def test_adding(self):
        adapter = IJournalEntryContainer(self.journal)
        adapter.add(JournalEntry(u'One', u'First journalentry.'))
        adapter.add(JournalEntry(u'Two', u'Second journalentry.'))
        adapter.add(JournalEntry(u'Three', u'Third journalentry.'))
        self.assertEqual(len(adapter), 3)

        # check the first journalentry
        self.assertEqual(adapter[0].creator, 'test_user_1_')
        self.assertTrue(isinstance(adapter[0].created, datetime))
        self.assertTrue(isinstance(adapter[0].modified, datetime))
        self.assertEqual(adapter[0].created, adapter[0].modified)
        self.assertEqual(adapter[0].title, u'One')
        self.assertEqual(adapter[0].text, u'First journalentry.')

        # dates are sequential
        self.assertTrue(adapter[0].created < adapter[1].created)
        self.assertTrue(adapter[1].created < adapter[2].created)

        # check the other journal-entries
        self.assertEqual(adapter[1].title, u'Two')
        self.assertEqual(adapter[2].title, u'Three')
        self.assertEqual(adapter[1].text, u'Second journalentry.')
        self.assertEqual(adapter[2].text, u'Third journalentry.')
