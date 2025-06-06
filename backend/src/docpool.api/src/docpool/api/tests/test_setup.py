from docpool.api.testing import DOCPOOL_API_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.base.utils import get_installer

import unittest


class TestSetup(unittest.TestCase):
    """Test that docpool.api is properly installed."""

    layer = DOCPOOL_API_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal)

    def test_product_installed(self):
        """Test if docpool.api is installed."""
        self.assertTrue(self.installer.is_product_installed("docpool.api"))

    def test_browserlayer(self):
        """Test that IDocpoolApiLayer is registered."""
        from docpool.api.interfaces import IDocpoolApiLayer
        from plone.browserlayer import utils

        self.assertIn(IDocpoolApiLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):
    layer = DOCPOOL_API_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.installer = get_installer(self.portal)
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        self.installer.uninstall_product("docpool.api")
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if docpool.api is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed("docpool.api"))

    def test_browserlayer_removed(self):
        """Test that IDocpoolApiLayer is removed."""
        from docpool.api.interfaces import IDocpoolApiLayer
        from plone.browserlayer import utils

        self.assertNotIn(IDocpoolApiLayer, utils.registered_layers())
