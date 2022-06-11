"""Setup tests for this package."""
from elan.esd.testing import ELAN_ESD_INTEGRATION_TESTING  # noqa: E501
from plone.base.utils import get_installer

import unittest

class TestSetup(unittest.TestCase):
    """Test that docpool.event is properly installed."""

    layer = ELAN_ESD_INTEGRATION_TESTING

    def test_product_installed(self):
        """Test if elan.esd is installed."""
        self.installer = get_installer(self.layer['portal'], self.layer['request'])
        self.assertTrue(self.installer.is_product_installed('elan.esd'))
