# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from elan.esd.testing import ELAN_ESD_INTEGRATION_TESTING  # noqa: E501
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None

class TestSetup(unittest.TestCase):
    """Test that docpool.event is properly installed."""

    layer = ELAN_ESD_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if elan.esd is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'elan.esd'))
