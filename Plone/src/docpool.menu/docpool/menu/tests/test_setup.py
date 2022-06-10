# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from docpool.menu.testing import DOCPOOL_MENU_INTEGRATION_TESTING  # noqa
from plone import api
from plone.base.utils import get_installer

import unittest


class TestSetup(unittest.TestCase):
    """Test that docpool.menu is properly installed."""

    layer = DOCPOOL_MENU_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = get_installer(self.portal)

    def test_product_installed(self):
        """Test if docpool.menu is installed."""
        self.assertTrue(self.installer.is_product_installed('docpool.menu'))

    def test_browserlayer(self):
        """Test that IDocpoolMenuLayer is registered."""
        from docpool.menu.interfaces import IDocpoolMenuLayer
        from plone.browserlayer import utils

        self.assertIn(IDocpoolMenuLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = DOCPOOL_MENU_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = get_installer(self.portal)
        self.installer.uninstall_product('docpool.menu')

    def test_product_uninstalled(self):
        """Test if docpool.menu is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed('docpool.menu'))

    def test_browserlayer_removed(self):
        """Test that IDocpoolMenuLayer is removed."""
        from docpool.menu.interfaces import IDocpoolMenuLayer
        from plone.browserlayer import utils

        self.assertNotIn(IDocpoolMenuLayer, utils.registered_layers())
