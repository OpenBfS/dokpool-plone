from docpool.ui.testing import DOCPOOL_UI_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class TestUI(unittest.TestCase):
    """Test that docpool.ui is properly installed."""

    layer = DOCPOOL_UI_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_listing_find_on_empty_docpool(self):
        listing_view = api.content.get_view("listing", self.portal, self.request)
        # Nothing found - no UIDs and no modified date
        self.assertEqual(listing_view.find(), ([], None))
