"""Setup tests for this package."""

from docpool.theme.browser.viewlets.common import LogoDocpoolViewlet
from docpool.ui.testing import DOCPOOL_UI_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.base.utils import get_installer

import unittest


class TestSetup(unittest.TestCase):
    """Test that docpool.UI is properly installed."""

    layer = DOCPOOL_UI_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.installer = get_installer(self.portal)
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_product_installed(self):
        """Test if docpool.api is installed."""
        self.assertTrue(self.installer.is_product_installed("docpool.ui"))

    def test_browserlayer(self):
        """Test that IDocpoolApiLayer is registered."""
        from docpool.ui.interfaces import IUITheme
        from plone.browserlayer import utils

        self.assertIn(IUITheme, utils.registered_layers())

    def test_debug_viewlet(self):
        self.request["URL"] = "http://nohost/plone/view"
        self.request["PARENTS"][0] = self.portal
        viewlet = LogoDocpoolViewlet(self.portal, self.request, None, None)
        self.assertTrue(viewlet.available())
        viewlet.update()
        html = viewlet.render()
        self.assertNotIn("Not detected", html)
        api.portal.set_registry_record(name="docpool.show_debug_info", value=False)
        # We disable the viewlet to test its availability
        self.assertFalse(viewlet.available())
