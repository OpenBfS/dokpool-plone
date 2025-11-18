"""Unit tests for local behavior components."""

from docpool.base.testing import DOCPOOL_BASE_INTEGRATION_TESTING
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from unittest.mock import Mock
from unittest.mock import patch
from zope.interface import Interface

import unittest


class TestLocalBehaviorSupport(unittest.TestCase):
    """Test the LocalBehaviorSupport adapter."""

    layer = DOCPOOL_BASE_INTEGRATION_TESTING

    def setUp(self):
        """Set up test environment."""
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

        # Create test document
        self.document = api.content.create(
            container=self.portal,
            type="Document",  # Use regular Document for simplicity
            id="test_document",
            title="Test Document",
        )

    def test_local_behaviors_property_getter_empty(self):
        """Test getting behaviors when none are set."""
        from docpool.base.localbehavior.localbehavior import LocalBehaviorSupport

        # Create adapter directly instead of using interface adaptation
        adapter = LocalBehaviorSupport(self.document)
        behaviors = adapter.local_behaviors

        self.assertIsInstance(behaviors, list)
        self.assertEqual(behaviors, [])

    def test_local_behaviors_property_getter_with_behaviors(self):
        """Test getting behaviors when some are set."""
        from docpool.base.localbehavior.localbehavior import LocalBehaviorSupport

        # Set behaviors directly on the object
        self.document.local_behaviors = ["test_app1", "test_app2"]

        adapter = LocalBehaviorSupport(self.document)
        behaviors = adapter.local_behaviors

        self.assertIsInstance(behaviors, list)
        self.assertEqual(set(behaviors), {"test_app1", "test_app2"})

    def test_local_behaviors_property_getter_deduplication(self):
        """Test that duplicate behaviors are deduplicated."""
        from docpool.base.localbehavior.localbehavior import LocalBehaviorSupport

        # Set behaviors with duplicates directly on the object
        self.document.local_behaviors = ["test_app1", "test_app2", "test_app1"]

        adapter = LocalBehaviorSupport(self.document)
        behaviors = adapter.local_behaviors

        self.assertEqual(len(behaviors), 2)
        self.assertEqual(set(behaviors), {"test_app1", "test_app2"})

    def test_local_behaviors_property_setter_list(self):
        """Test setting behaviors with a list."""
        from docpool.base.localbehavior.localbehavior import LocalBehaviorSupport

        adapter = LocalBehaviorSupport(self.document)
        test_behaviors = ["test_app1", "test_app2"]
        adapter.local_behaviors = test_behaviors

        # Check it was stored
        stored_behaviors = getattr(self.document, "local_behaviors", [])
        self.assertEqual(set(stored_behaviors), set(test_behaviors))

    def test_local_behaviors_property_setter_tuple(self):
        """Test setting behaviors with a tuple."""
        from docpool.base.localbehavior.localbehavior import LocalBehaviorSupport

        adapter = LocalBehaviorSupport(self.document)
        test_behaviors = ("test_app1", "test_app2")
        adapter.local_behaviors = test_behaviors

        # Check it was stored as list
        stored_behaviors = getattr(self.document, "local_behaviors", [])
        self.assertIsInstance(stored_behaviors, list)
        self.assertEqual(set(stored_behaviors), set(test_behaviors))

    def test_local_behaviors_property_setter_with_duplicates(self):
        """Test setting behaviors with duplicates removes them."""
        from docpool.base.localbehavior.localbehavior import LocalBehaviorSupport

        adapter = LocalBehaviorSupport(self.document)
        test_behaviors = ["test_app1", "test_app2", "test_app1", "test_app2"]
        adapter.local_behaviors = test_behaviors

        stored_behaviors = getattr(self.document, "local_behaviors", [])
        self.assertEqual(len(stored_behaviors), 2)
        self.assertEqual(set(stored_behaviors), {"test_app1", "test_app2"})

    def test_local_behaviors_property_setter_none(self):
        """Test setting behaviors to None clears them."""
        from docpool.base.localbehavior.localbehavior import LocalBehaviorSupport

        # First set some behaviors
        self.document.local_behaviors = ["test_app1", "test_app2"]

        adapter = LocalBehaviorSupport(self.document)
        adapter.local_behaviors = None

        stored_behaviors = getattr(self.document, "local_behaviors", [])
        self.assertEqual(stored_behaviors, [])

    def test_local_behaviors_property_setter_empty_list(self):
        """Test setting behaviors to empty list."""
        from docpool.base.localbehavior.localbehavior import LocalBehaviorSupport

        # First set some behaviors
        self.document.local_behaviors = ["test_app1", "test_app2"]

        adapter = LocalBehaviorSupport(self.document)
        adapter.local_behaviors = []

        stored_behaviors = getattr(self.document, "local_behaviors", [])
        self.assertEqual(stored_behaviors, [])


class TestInitializeLocalBehaviors(unittest.TestCase):
    """Test the initializeLocalBehaviors default factory function."""

    layer = DOCPOOL_BASE_INTEGRATION_TESTING

    def setUp(self):
        """Set up test environment."""
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    @patch("docpool.base.localbehavior.localbehavior.getMultiAdapter")
    @patch("docpool.base.localbehavior.localbehavior.getRequest")
    def test_returns_effective_apps(self, mock_get_request, mock_get_adapter):
        """Test that initializeLocalBehaviors returns effective apps."""
        from docpool.base.localbehavior.localbehavior import initializeLocalBehaviors

        # Mock request and app state
        mock_request = Mock()
        mock_get_request.return_value = mock_request

        mock_app_state = Mock()
        mock_app_state.effectiveAppsHere.return_value = ["test_app1", "test_app2"]
        mock_get_adapter.return_value = mock_app_state

        # Create test context
        context = self.portal

        # Call function
        result = initializeLocalBehaviors(context)

        # Verify calls
        mock_get_adapter.assert_called_once_with((context, mock_request), name="dp_app_state")
        mock_app_state.effectiveAppsHere.assert_called_once()

        # Verify result
        self.assertEqual(result, ["test_app1", "test_app2"])

    @patch("docpool.base.localbehavior.localbehavior.getMultiAdapter")
    @patch("docpool.base.localbehavior.localbehavior.getRequest")
    def test_returns_empty_list_when_no_apps(self, mock_get_request, mock_get_adapter):
        """Test handling of empty effective apps."""
        from docpool.base.localbehavior.localbehavior import initializeLocalBehaviors

        # Mock request and app state with no apps
        mock_request = Mock()
        mock_get_request.return_value = mock_request

        mock_app_state = Mock()
        mock_app_state.effectiveAppsHere.return_value = []
        mock_get_adapter.return_value = mock_app_state

        context = self.portal
        result = initializeLocalBehaviors(context)

        self.assertEqual(result, [])


class TestIsSupportedFunction(unittest.TestCase):
    """Test the isSupported utility function."""

    def setUp(self):
        """Set up test interfaces."""

        # Create test interfaces
        class ITestExtension(Interface):
            """Test extension interface."""

            pass

        class ITestCoreInterface(Interface):
            """Test core interface."""

            pass

        # Make ITestExtension extend IExtension
        from docpool.base.interfaces import IExtension

        ITestExtension.__bases__ = (IExtension,)

        self.extension_interface = ITestExtension
        self.core_interface = ITestCoreInterface

    @patch("docpool.base.localbehavior.adapter.BEHAVIOR_REGISTRY")
    def test_extension_behavior_supported(self, mock_registry):
        """Test extension behavior with matching apps."""
        from docpool.base.localbehavior.adapter import isSupported

        # Mock behavior registry
        mock_registry.get.return_value = ["test_app1", "test_app2"]

        available_apps = ["test_app1", "test_app3"]
        result = isSupported(available_apps, self.extension_interface)

        # Should return intersection
        self.assertEqual(result, {"test_app1"})

    @patch("docpool.base.localbehavior.adapter.BEHAVIOR_REGISTRY")
    def test_extension_behavior_not_supported(self, mock_registry):
        """Test extension behavior with no matching apps."""
        from docpool.base.localbehavior.adapter import isSupported

        mock_registry.get.return_value = ["test_app1", "test_app2"]

        available_apps = ["test_app3", "test_app4"]
        result = isSupported(available_apps, self.extension_interface)

        # Should return empty set
        self.assertEqual(result, set())

    def test_extension_behavior_no_available_apps(self):
        """Test extension behavior with no available apps."""
        from docpool.base.localbehavior.adapter import isSupported

        available_apps = []
        result = isSupported(available_apps, self.extension_interface)

        # Should return False
        self.assertFalse(result)

    def test_core_behavior_always_supported(self):
        """Test that core behaviors are always supported."""
        from docpool.base.localbehavior.adapter import isSupported

        available_apps = []  # Even with no apps
        result = isSupported(available_apps, self.core_interface)

        # Should always be True
        self.assertTrue(result)

    def test_core_behavior_supported_with_apps(self):
        """Test core behavior with available apps."""
        from docpool.base.localbehavior.adapter import isSupported

        available_apps = ["test_app1", "test_app2"]
        result = isSupported(available_apps, self.core_interface)

        # Should always be True
        self.assertTrue(result)
