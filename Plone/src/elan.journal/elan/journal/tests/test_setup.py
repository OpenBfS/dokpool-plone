# -*- coding: utf-8 -*-
from elan.journal.config import PROJECTNAME
from elan.journal.interfaces import IBrowserLayer
from elan.journal.testing import INTEGRATION_TESTING
from plone.base.utils import get_installer
from plone.browserlayer.utils import registered_layers

import unittest


ADD_PERMISSIONS = (
    dict(
        title='elan.journal: Add Journal',
        expected=[
            'ContentAdmin',
            'DocPoolAdmin',
            'EventEditor',
            'JournalEditor',
            'Manager',
            'Site Administrator',
            ],
    ),
    dict(
        title='elan.journal: Add JournalEntry',
        expected=[
            'ContentAdmin',
            'DocPoolAdmin',
            'EventEditor',
            'JournalEditor',
            'Manager',
            'Site Administrator',
            ],
    ),
)


class InstallTestCase(unittest.TestCase):

    """Ensure product is properly installed."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = get_installer(self.portal)

    def test_installed(self):
        self.assertTrue(self.installer.is_product_installed(PROJECTNAME))

    def test_browser_layer_installed(self):
        self.assertIn(IBrowserLayer, registered_layers())

    def test_add_permissions(self):
        for permission in ADD_PERMISSIONS:
            roles = self.portal.rolesOfPermission(permission['title'])
            roles = [r['name'] for r in roles if r['selected']]
            self.assertListEqual(roles, permission['expected'])

class UninstallTestCase(unittest.TestCase):

    """Ensure product is properly uninstalled."""

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = get_installer(self.portal)
        self.installer.uninstall_product(PROJECTNAME)

    def test_uninstalled(self):
        self.assertFalse(self.installer.is_product_installed(PROJECTNAME))

    def test_browser_layer_removed(self):
        self.assertNotIn(IBrowserLayer, registered_layers())
