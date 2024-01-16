from docpool.elan.testing import DOCPOOL_EVENT_FUNCTIONAL_TESTING
from plone.app.testing import login
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.testing.zope import Browser

import unittest


class TestTickerFunctional(unittest.TestCase):
    layer = DOCPOOL_EVENT_FUNCTIONAL_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.portal_url = self.portal.absolute_url()
        self.browser = Browser(app)
        self.browser.handleErrors = False
        login(self.portal, SITE_OWNER_NAME)

    def test_ticker(self):
        self.browser.addHeader(
            "Authorization",
            f"Basic {SITE_OWNER_NAME}:{SITE_OWNER_PASSWORD}",
        )
        login(self.portal, SITE_OWNER_NAME)
        # Switch to elan
        self.browser.open(self.portal_url + "/test_docpool/esd/setActiveApp?app=elan")
        # We can now see the elanlogo
        self.assertIn("elanlogo.png", self.browser.contents)
        # No ticker text for now
        self.assertNotIn('<aside class="marquee">', self.browser.contents)
        # Add a ticker text
        self.browser.open(self.portal_url + "/test_docpool/contentconfig/ticker/edit")
        form_field = self.browser.getControl(name="form.widgets.text")
        form_field.value = "Important Ticker - do not touch"
        # Save
        self.browser.getControl(name="form.buttons.save").click()
        # Saved correctly
        self.assertIn("Important Ticker - do not touch", self.browser.contents)
        # Now with marquee ticker
        self.assertIn('<aside class="marquee">', self.browser.contents)
