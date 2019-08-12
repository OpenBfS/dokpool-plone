# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from docpool.doksys.testing import DOCPOOL_DOKSYS_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class TestSetup(unittest.TestCase):
    """Test that docpool.doksys is properly installed."""

    layer = DOCPOOL_DOKSYS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if docpool.doksys is installed."""
        self.assertTrue(self.installer.isProductInstalled('docpool.doksys'))

    def test_browserlayer(self):
        """Test that IDocpoolDoksysLayer is registered."""
        from docpool.doksys.interfaces import IDocpoolDoksysLayer
        from plone.browserlayer import utils

        self.assertIn(IDocpoolDoksysLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = DOCPOOL_DOKSYS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['docpool.doksys'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if docpool.doksys is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled('docpool.doksys'))

    def test_browserlayer_removed(self):
        """Test that IDocpoolDoksysLayer is removed."""
        from docpool.doksys.interfaces import IDocpoolDoksysLayer
        from plone.browserlayer import utils

        self.assertNotIn(IDocpoolDoksysLayer, utils.registered_layers())
