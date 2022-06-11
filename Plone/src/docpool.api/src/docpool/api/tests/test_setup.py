"""Setup tests for this package."""
from docpool.api.testing import DOCPOOL_API_FUNCTIONAL_FULL_TESTING  # noqa
from docpool.api.testing import DOCPOOL_API_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import TEST_USER_ID
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.z3cform.interfaces import IPloneFormLayer
from plone.base.utils import get_installer
from zope.interface.declarations import alsoProvides
import unittest


class TestSetup(unittest.TestCase):
    """Test that docpool.api is properly installed."""

    layer = DOCPOOL_API_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = get_installer(self.portal)

    def test_product_installed(self):
        """Test if docpool.api is installed."""
        self.assertTrue(self.installer.is_product_installed('docpool.api'))

    def test_browserlayer(self):
        """Test that IDocpoolApiLayer is registered."""
        from docpool.api.interfaces import IDocpoolApiLayer
        from plone.browserlayer import utils

        self.assertIn(IDocpoolApiLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = DOCPOOL_API_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = get_installer(self.portal)
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstall_product('docpool.api')
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if docpool.api is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed('docpool.api'))

    def test_browserlayer_removed(self):
        """Test that IDocpoolApiLayer is removed."""
        from docpool.api.interfaces import IDocpoolApiLayer
        from plone.browserlayer import utils

        self.assertNotIn(IDocpoolApiLayer, utils.registered_layers())


class TestInstallComplex(unittest.TestCase):
    """Test installation of @@docpool_setup into Plone for complex tests."""

    layer = DOCPOOL_API_FUNCTIONAL_FULL_TESTING
    level = 4

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.request, IPloneFormLayer)
        login(self.portal, SITE_OWNER_NAME)

    def test_demo_setup(self):
        portal_catalog = api.portal.get_tool('portal_catalog')
        self.request.form['submit'] = True
        view = api.content.get_view(
            name='docpool_setup',
            context=self.portal,
            request=self.request,
        )
        result = view()
        # We now have two DocumentPool (bund & hessen)
        self.assertEqual(
            2,
            len(portal_catalog.unrestrictedSearchResults(portal_type='DocumentPool')))