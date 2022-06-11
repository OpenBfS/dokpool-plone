"""Test case for viewlets on the package.

For more information on how to test viewlets, see:
http://developer.plone.org/views/viewlets.html#finding-viewlets-programmatically
"""
from elan.journal.interfaces import IBrowserLayer
from elan.journal.testing import INTEGRATION_TESTING
from plone import api
from Products.Five.browser import BrowserView as View
from zope.component import queryMultiAdapter
from zope.interface import alsoProvides
from zope.viewlet.interfaces import IViewletManager

import unittest


class ViewletTestCase(unittest.TestCase):

    """Tests for viewlets."""

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

    def _get_viewlet_manager(self):
        context = self.journal
        request = self.request
        view = View(context, request)
        manager = queryMultiAdapter(
            (context, request, view), IViewletManager, 'plone.abovecontent'
        )

        return manager

    def test_viewlet_is_registered(self):
        manager = self._get_viewlet_manager()
        self.assertTrue(manager)
        manager.update()
        self.assertIn('elan.journal.header', manager)

    def test_viewlet_order(self):
        manager = self._get_viewlet_manager()
        manager.update()
        self.assertEqual(len(manager.viewlets), 2)
        viewlets = [v.__name__ for v in manager.viewlets]
        self.assertListEqual(viewlets, ['elan.journal.header', 'docpool.path_bar'])

    def test_viewlet_is_available(self):
        from plone.namedfile.file import NamedBlobImage

        manager = self._get_viewlet_manager()
        manager.update()
        viewlet = manager['elan.journal.header']
        viewlet.update()
        self.assertFalse(viewlet.available())
        self.journal.image = NamedBlobImage()
        self.assertTrue(viewlet.available())

        # default view
        self.request['URL'] = 'http://nohost/plone/journal/view'
        self.request['PARENTS'][0] = self.journal
        self.assertTrue(viewlet.available())

        # journalentry view
        self.request.path = ['1462277979.55']
        self.request['URL'] = 'http://nohost/plone/journal/journalentry/1462277979.55'
        view = api.content.get_view('journalentry', self.journal, self.request)
        self.request['PARENTS'][0] = view
        self.assertFalse(viewlet.available())
