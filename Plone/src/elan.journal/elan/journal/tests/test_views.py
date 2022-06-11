from DateTime import DateTime
from datetime import datetime
from datetime import timedelta
from elan.journal.interfaces import IBrowserLayer
from elan.journal.testing import INTEGRATION_TESTING
from elan.journal.tests.utils import _create_journalentries
from plone import api
from time import time
from zExceptions import NotFound
from zope.interface import alsoProvides

import unittest


class ViewTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.request, IBrowserLayer)
        docpool = self.portal['test_docpool']
        self.container = docpool['contentconfig']['scen']['routinemode']
        with api.env.adopt_roles(['Manager']):
            self.journal = api.content.create(
                self.container, 'Journal', 'journal')


class DefaultViewTestCase(ViewTestCase):
    def setUp(self):
        super().setUp()
        self.view = api.content.get_view('view', self.journal, self.request)

    def test_has_updates(self):
        self.assertFalse(self.view.has_updates)
        _create_journalentries(self.journal, 1)
        self.assertTrue(self.view.has_updates)

    def test_automatic_updates_enabled(self):
        self.assertTrue(self.view.automatic_updates_enabled)
        self.journal.modification_date = DateTime() - 3
        self.assertFalse(self.view.automatic_updates_enabled)
        self.journal.modification_date = DateTime()
        self.assertTrue(self.view.automatic_updates_enabled)

    def test_date_is_shown_in_journalentries_older_than_today(self):
        # comment inside the JS block that adds the dates
        comment = '/* show dates for journal-entries older than today */'
        self.assertIn(comment, self.view())
        self.journal.modification_date = DateTime() - 3
        self.assertIn(comment, self.view())
        self.journal.modification_date = DateTime()
        self.assertIn(comment, self.view())

    def test_rendered(self):
        _create_journalentries(self.journal, 1)
        timestamp = self.journal.get_journalentries()[0]['timestamp']
        rendered = self.view()
        link = f'http://nohost/plone/test_docpool/contentconfig/scen/routinemode/journal/journalentry/{timestamp}'
        self.assertIn(f'<a href="{link}">', rendered)


class JournalEntryViewTestCase(ViewTestCase):
    def test_no_timestamp_raises_bad_request(self):
        self.request.path = []
        view = api.content.get_view('journalentry', self.journal, self.request)
        self.assertEqual(view(), '')
        self.assertEqual(self.request.RESPONSE.getStatus(), 400)

    def test_invalid_timestamp_raises_not_found(self):
        self.request.path = ['asdf']
        view = api.content.get_view('journalentry', self.journal, self.request)
        with self.assertRaises(NotFound):
            view.publishTraverse(self.request, 'asdf')

    def test_rendered(self):
        _create_journalentries(self.journal, 1)
        timestamp = self.journal.get_journalentries()[0]['timestamp']
        self.request.path = [timestamp]
        view = api.content.get_view('journalentry', self.journal, self.request)
        view.publishTraverse(self.request, timestamp)
        rendered = view()
        self.assertIn('itemtype="http://schema.org/BlogPosting"', rendered)
        self.assertIn(
            '<span property="rnews:author">test-user</span>',
            rendered)
        self.assertIn('<span property="rnews:datePublished">', rendered)
        self.assertNotIn('<span property="rnews:dateModified">', rendered)
        self.assertIn(f'data-timestamp="{timestamp}"', rendered)


class UpdateViewTestCase(ViewTestCase):
    def setUp(self):
        super().setUp()
        self.view = api.content.get_view('update', self.journal, self.request)

    def test_view_listed_in_actions(self):
        portal_types = api.portal.get_tool('portal_types')
        actions = portal_types['Journal'].listActions()
        actions = [a.id for a in actions]
        self.assertIn('update', actions)

    def test_date_is_shown_in_journalentries_older_than_today(self):
        # comment inside the JS block that adds the dates
        comment = '/* show dates for journal-entries older than today */'
        self.assertIn(comment, self.view())
        self.journal.modification_date = DateTime() - 3
        self.assertIn(comment, self.view())
        self.journal.modification_date = DateTime()
        self.assertIn(comment, self.view())


class RecentUpdatesViewTestCase(ViewTestCase):
    def setUp(self):
        super().setUp()
        self.view = api.content.get_view(
            'recent-updates', self.journal, self.request)

    def test_needs_hard_refresh_on_edition(self):
        # an edition happened before last update; we already handled it
        self.journal._last_journalentry_edition = str(time() - 120)
        self.assertFalse(self.view._needs_hard_refresh())
        # an edition happened after last update; we need to handle it
        self.journal._last_journalentry_edition = str(time() - 30)
        self.assertTrue(self.view._needs_hard_refresh())
        self.assertEqual(self.request.RESPONSE.getStatus(), 205)

    def test_needs_hard_refresh_on_deletion(self):
        # a deletion happened before last update; we already handled it
        self.journal._last_journalentry_deletion = str(time() - 120)
        self.assertFalse(self.view._needs_hard_refresh())
        # a deletion happened after last update; we need to handle it
        self.journal._last_journalentry_deletion = str(time() - 30)
        self.assertTrue(self.view._needs_hard_refresh())
        self.assertEqual(self.request.RESPONSE.getStatus(), 205)

    def test_not_modified(self):
        RFC1123 = '%a, %d %b %Y %H:%M:%S GMT'
        # calling the method without header will return False
        assert not self.request.get_header('If-Modified-Since')
        self.assertFalse(self.view._not_modified())
        # invalid date return False
        self.request.environ['IF_MODIFIED_SINCE'] = 'invalid'
        assert self.request.get_header('If-Modified-Since') == 'invalid'
        self.assertFalse(self.view._not_modified())
        # modified, return False as we must update
        if_modified_since = datetime.utcnow() - timedelta(seconds=60)
        if_modified_since = if_modified_since.strftime(RFC1123)
        self.request.environ['IF_MODIFIED_SINCE'] = if_modified_since
        self.assertFalse(self.view._not_modified())
        # not modified, return True and set header
        if_modified_since = datetime.utcnow() + timedelta(seconds=60)
        if_modified_since = if_modified_since.strftime(RFC1123)
        self.request.environ['IF_MODIFIED_SINCE'] = if_modified_since
        self.assertTrue(self.view._not_modified())
        self.assertEqual(self.request.RESPONSE.getStatus(), 304)

    # def test_get_latest_journalentries(self):
    #     from time import sleep

    #     _create_journalentries(self.journal, 10)
    #     self.assertEqual(len(self.view.get_latest_journalentries()), 10)
    #     # after one minutes no journal.entreis should be listed
    #     sleep(60)  # WT actual F?
    #     self.assertEqual(len(self.view.get_latest_journalentries()), 0)
    #     # if we add more journal-entries, they should be listed
    #     _create_journalentries(self.journal, 5)
    #     self.assertEqual(len(self.view.get_latest_journalentries()), 5)
