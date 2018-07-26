# -*- coding: utf-8 -*-
from elan.journal.config import PROJECTNAME
from elan.journal.interfaces import IBrowserLayer
from elan.journal.testing import INTEGRATION_TESTING
from elan.journal.testing import IS_PLONE_5
from plone.browserlayer.utils import registered_layers

import unittest


CSS = '++resource++elan.journal/styles.css'

ADD_PERMISSIONS = (
    dict(
        title='elan.journal: Add Journal',
        expected=['Contributor', 'Manager', 'Owner', 'Site Administrator'],
    ),
    dict(
        title='elan.journal: Add JournalEntry',
        expected=['Editor', 'Manager', 'Owner', 'Site Administrator'],
    ),
)


class InstallTestCase(unittest.TestCase):

    """Ensure product is properly installed."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME))

    def test_browser_layer_installed(self):
        self.assertIn(IBrowserLayer, registered_layers())

    @unittest.skipIf(IS_PLONE_5, 'No easy way to test this under Plone 5')
    def test_cssregistry(self):
        resource_ids = self.portal.portal_css.getResourceIds()
        self.assertIn(CSS, resource_ids)

    def test_add_permissions(self):
        for permission in ADD_PERMISSIONS:
            roles = self.portal.rolesOfPermission(permission['title'])
            roles = [r['name'] for r in roles if r['selected']]
            self.assertListEqual(roles, permission['expected'])

    @unittest.skipIf(IS_PLONE_5, 'Not needed in Plone 5')
    def test_tinymce_is_linkable(self):
        tinymce = self.portal['portal_tinymce']
        self.assertIn('Journal', tinymce.linkable.split('\n'))


class UninstallTestCase(unittest.TestCase):

    """Ensure product is properly uninstalled."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_browser_layer_removed(self):
        self.assertNotIn(IBrowserLayer, registered_layers())

    @unittest.skipIf(IS_PLONE_5, 'No easy way to test this under Plone 5')
    def test_cssregistry_removed(self):
        resource_ids = self.portal.portal_css.getResourceIds()
        self.assertNotIn(CSS, resource_ids)
