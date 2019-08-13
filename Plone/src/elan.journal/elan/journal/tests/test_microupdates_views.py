# -*- coding: utf-8 -*-
from elan.journal.adapters import IJournalEntryContainer
from elan.journal.adapters import JournalEntry
from elan.journal.interfaces import IBrowserLayer
from elan.journal.testing import INTEGRATION_TESTING
from plone import api
from Products.statusmessages.interfaces import IStatusMessage
from zope.interface import alsoProvides

import unittest


class BaseJournalEntryViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.request, IBrowserLayer)
        with api.env.adopt_roles(['Manager']):
            self.journal = api.content.create(
                self.portal, 'Journal', 'journal')
        self.view = api.content.get_view(
            'base-journalentry', self.journal, self.request
        )
        adapter = IJournalEntryContainer(self.journal)
        adapter.add(JournalEntry(u'', u'Check me!'))

    def test_validate_journalentry_id(self):
        self.request.form['id'] = '0'
        valid = self.view._validate_journalentry_id()
        self.assertTrue(valid)

    def test_validate_journalentry_no_id(self):
        valid = self.view._validate_journalentry_id()
        self.assertFalse(valid)
        msg = IStatusMessage(self.request).show()
        self.assertEqual(len(msg), 1)
        expected = u'No journalentry selected.'
        self.assertEqual(msg[0].message, expected)

    def test_validate_journalentry_invalid_id(self):
        self.request.form['id'] = 'invalid'
        valid = self.view._validate_journalentry_id()
        self.assertFalse(valid)
        msg = IStatusMessage(self.request).show()
        self.assertEqual(len(msg), 1)
        expected = u'Journalentry id is not an integer.'
        self.assertEqual(msg[0].message, expected)

    def test_validate_journalentry_id_greater_than_lenght(self):
        self.request.form['id'] = '2'
        valid = self.view._validate_journalentry_id()
        self.assertFalse(valid)
        msg = IStatusMessage(self.request).show()
        self.assertEqual(len(msg), 1)
        expected = u'Journalentry id does not exist.'
        self.assertEqual(msg[0].message, expected)


class AddJournalEtnryViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.request, IBrowserLayer)
        with api.env.adopt_roles(['Manager']):
            self.journal = api.content.create(
                self.portal, 'Journal', 'journal')

    def test_add_journalentry_no_parameters(self):
        self.journal.unrestrictedTraverse('add-journalentry')()
        # status message is set
        msg = IStatusMessage(self.request).show()
        self.assertEqual(len(msg), 1)
        expected = u'Required text input is missing.'
        self.assertEqual(msg[0].message, expected)
        # redirection will happen
        self.assertEqual(
            self.request.RESPONSE.getHeader('location'),
            'http://nohost/plone/journal/update',
        )

    def test_add_journalentry(self):
        self.request.form['title'] = ''
        self.request.form['text'] = 'Extra! Extra! Read All About It!'
        self.journal.unrestrictedTraverse('add-journalentry')()
        # status message is set
        msg = IStatusMessage(self.request).show()
        self.assertEqual(len(msg), 1)
        expected = u'Item published.'
        self.assertEqual(msg[0].message, expected)
        # redirection will happen
        self.assertEqual(
            self.request.RESPONSE.getHeader('location'),
            'http://nohost/plone/journal/update',
        )


class EditJournalEntryViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.request, IBrowserLayer)
        with api.env.adopt_roles(['Manager']):
            self.journal = api.content.create(
                self.portal, 'Journal', 'journal')
        adapter = IJournalEntryContainer(self.journal)
        adapter.add(JournalEntry(u'', u'Edit me!'))

    def test_edit_journalentry(self):
        self.request.form['id'] = '0'
        self.request.form['text'] = 'Edited!'
        self.request.form['form.buttons.save'] = 'Save'
        self.journal.unrestrictedTraverse('edit-journalentry')()
        # journal was updated
        self.assertNotEqual(self.journal._last_journalentry_edition, '0.0')
        # journalentry was modified
        adapter = IJournalEntryContainer(self.journal)
        self.assertEqual(adapter[0].text, 'Edited!')
        # status message is set
        msg = IStatusMessage(self.request).show()
        self.assertEqual(len(msg), 1)
        expected = u'Item saved.'
        self.assertEqual(msg[0].message, expected)
        # redirection will happen
        self.assertEqual(
            self.request.RESPONSE.getHeader('location'),
            'http://nohost/plone/journal/update',
        )


class DeleteJournalEntryViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.request, IBrowserLayer)
        with api.env.adopt_roles(['Manager']):
            self.journal = api.content.create(
                self.portal, 'Journal', 'journal')
        adapter = IJournalEntryContainer(self.journal)
        adapter.add(JournalEntry(u'', u'Delete me!'))

    def test_delete_journalentry(self):
        self.request.form['id'] = '0'
        self.journal.unrestrictedTraverse('delete-journalentry')()
        # journal was updated
        self.assertNotEqual(self.journal._last_journalentry_deletion, '0.0')
        # journalentry was deleted
        adapter = IJournalEntryContainer(self.journal)
        self.assertIsNone(adapter[0])
        # status message is set
        msg = IStatusMessage(self.request).show()
        self.assertEqual(len(msg), 1)
        expected = u'Item deleted.'
        self.assertEqual(msg[0].message, expected)
        # redirection will happen
        self.assertEqual(
            self.request.RESPONSE.getHeader('location'),
            'http://nohost/plone/journal/update',
        )
