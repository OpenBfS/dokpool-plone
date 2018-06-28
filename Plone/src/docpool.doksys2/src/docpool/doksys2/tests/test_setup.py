# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from docpool.doksys2.testing import DOCPOOL_DOKSYS2_INTEGRATION_TESTING  # noqa

import unittest


class TestSetup(unittest.TestCase):
    """Test that docpool.doksys2 is properly installed."""

    layer = DOCPOOL_DOKSYS2_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if docpool.doksys2 is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'docpool.doksys2'))

    def test_browserlayer(self):
        """Test that IDocpoolDoksys2Layer is registered."""
        from docpool.doksys2.interfaces import (
            IDocpoolDoksys2Layer)
        from plone.browserlayer import utils
        self.assertIn(
            IDocpoolDoksys2Layer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = DOCPOOL_DOKSYS2_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstallProducts(['docpool.doksys2'])
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if docpool.doksys2 is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'docpool.doksys2'))

    def test_browserlayer_removed(self):
        """Test that IDocpoolDoksys2Layer is removed."""
        from docpool.doksys2.interfaces import \
            IDocpoolDoksys2Layer
        from plone.browserlayer import utils
        self.assertNotIn(
            IDocpoolDoksys2Layer,
            utils.registered_layers())
