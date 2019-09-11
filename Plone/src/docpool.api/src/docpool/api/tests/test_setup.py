# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from docpool.api.testing import DOCPOOL_API_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class TestSetup(unittest.TestCase):
    """Test that docpool.api is properly installed."""

    layer = DOCPOOL_API_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if docpool.api is installed."""
        self.assertTrue(self.installer.isProductInstalled('docpool.api'))

    def test_browserlayer(self):
        """Test that IDocpoolApiLayer is registered."""
        from docpool.api.interfaces import IDocpoolApiLayer
        from plone.browserlayer import utils

        self.assertIn(IDocpoolApiLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = DOCPOOL_API_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['docpool.api'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if docpool.api is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled('docpool.api'))

    def test_browserlayer_removed(self):
        """Test that IDocpoolApiLayer is removed."""
        from docpool.api.interfaces import IDocpoolApiLayer
        from plone.browserlayer import utils

        self.assertNotIn(IDocpoolApiLayer, utils.registered_layers())
