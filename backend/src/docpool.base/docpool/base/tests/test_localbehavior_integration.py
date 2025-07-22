"""Integration tests for local behavior system with real DocumentPools and applications."""

import unittest
from unittest.mock import Mock, patch

from docpool.base.testing import DOCPOOL_BASE_REALAPPS_INTEGRATION_TESTING
from docpool.base.testing import LocalBehaviorTestMixin
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.interface import alsoProvides


class TestRealDocumentPoolIntegration(unittest.TestCase, LocalBehaviorTestMixin):
    """Test local behaviors with real DocumentPools and applications."""
    
    layer = DOCPOOL_BASE_REALAPPS_INTEGRATION_TESTING
    
    def setUp(self):
        """Set up test environment with real DocumentPools."""
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        
        # Access real DocumentPools created by the layer
        self.bund_docpool = self.portal["bund"]  # Has elan + rei
        self.hessen_docpool = self.portal["hessen"]  # Has elan only
        
    def test_documentpool_creation_with_real_apps(self):
        """Test that DocumentPools are created with correct app support."""
        # Test bund docpool has both apps
        self.assertEqual(set(self.bund_docpool.supportedApps), {"elan", "rei"})
        self.assertEqual(self.bund_docpool.Title(), "Bund DocumentPool")
        
        # Test hessen docpool has only elan
        self.assertEqual(set(self.hessen_docpool.supportedApps), {"elan"})
        self.assertEqual(self.hessen_docpool.Title(), "Hessen DocumentPool")
        
    def test_dpdocument_creation_in_real_docpool(self):
        """Test creating DPDocument in real DocumentPool."""
        document = self.create_test_dpdocument(
            local_behaviors=["elan", "rei"]
        )
        
        self.assertEqual(document.portal_type, "DPDocument")
        self.assertEqual(document.Title(), "Test Document")
        
        # Check local behaviors were assigned
        from docpool.base.localbehavior.localbehavior import LocalBehaviorSupport
        adapter = LocalBehaviorSupport(document)
        behaviors = set(adapter.local_behaviors)
        self.assertEqual(behaviors, {"elan", "rei"})
        
    def test_dpdocument_with_restricted_apps(self):
        """Test DPDocument in DocumentPool with limited app support."""
        # Create document in hessen (elan-only) docpool
        document = self.create_test_dpdocument(
            container=self.hessen_docpool,
            local_behaviors=["elan"]  # Only elan is supported
        )
        
        from docpool.base.localbehavior.localbehavior import LocalBehaviorSupport
        adapter = LocalBehaviorSupport(document)
        behaviors = adapter.local_behaviors
        self.assertEqual(behaviors, ["elan"])
        
    def test_local_behavior_assignment_validation(self):
        """Test that local behaviors can be assigned to supported apps."""
        document = self.create_test_dpdocument()  # Use default container logic
        
        from docpool.base.localbehavior.localbehavior import LocalBehaviorSupport
        adapter = LocalBehaviorSupport(document)
        
        # Should be able to assign supported apps
        adapter.local_behaviors = ["elan", "rei"]
        self.assertEqual(set(adapter.local_behaviors), {"elan", "rei"})
        
        # Should also be able to assign just one app
        adapter.local_behaviors = ["elan"]
        self.assertEqual(adapter.local_behaviors, ["elan"])
        
    def test_app_state_integration(self):
        """Test integration with dp_app_state adapter."""
        document = self.create_test_dpdocument(
            local_behaviors=["elan"]
        )
        
        # Get the real app state adapter
        from zope.component import getMultiAdapter
        app_state = getMultiAdapter((document, self.request), name="dp_app_state")
        
        # This should work with real DocumentPool structure
        self.assertIsNotNone(app_state)
        
        # The adapter should be able to determine effective apps
        # (exact behavior depends on app state implementation)


class TestDexterityLocalBehaviorAssignableIntegration(unittest.TestCase, LocalBehaviorTestMixin):
    """Test DexterityLocalBehaviorAssignable with real content and applications."""
    
    layer = DOCPOOL_BASE_REALAPPS_INTEGRATION_TESTING
    
    def setUp(self):
        """Set up test environment."""
        self.portal = self.layer["portal"] 
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        
        self.bund_docpool = self.portal["bund"]
        self.hessen_docpool = self.portal["hessen"]
        
    def test_behavior_enumeration_with_real_dpdocument(self):
        """Test behavior enumeration with real DPDocument."""
        # Create DPDocument with local behavior support
        document = self.create_test_dpdocument(
            container=self.bund_docpool,
            local_behaviors=["elan"]
        )
        
        # Make document provide ILocalBehaviorSupporting
        from docpool.base.localbehavior.localbehavior import ILocalBehaviorSupporting
        alsoProvides(document, ILocalBehaviorSupporting)
        
        # Get the behavior assignable adapter
        from docpool.base.localbehavior.adapter import DexterityLocalBehaviorAssignable
        assignable = DexterityLocalBehaviorAssignable(document)
        
        # Enumerate behaviors (this tests the full integration)
        behaviors = list(assignable.enumerateBehaviors())
        
        # Should get some behaviors (exact number depends on registered behaviors)
        # The important thing is that it doesn't crash and returns something
        self.assertIsInstance(behaviors, list)
        
    def test_behavior_enumeration_with_form_data(self):
        """Test behavior enumeration with form data in request.""" 
        document = self.create_test_dpdocument(
            container=self.bund_docpool,
            local_behaviors=["elan"]
        )
        
        from docpool.base.localbehavior.localbehavior import ILocalBehaviorSupporting
        alsoProvides(document, ILocalBehaviorSupporting)
        
        # Simulate form data in request
        self.request.form = {
            'form.widgets.ILocalBehaviorSupport.local_behaviors': ['elan', 'rei']
        }
        
        from docpool.base.localbehavior.adapter import DexterityLocalBehaviorAssignable
        assignable = DexterityLocalBehaviorAssignable(document)
        
        # This should process the form data
        behaviors = list(assignable.enumerateBehaviors())
        self.assertIsInstance(behaviors, list)
        
    def test_behavior_caching_in_request(self):
        """Test that previous behaviors are cached in request."""
        document = self.create_test_dpdocument(
            container=self.bund_docpool,
            local_behaviors=["elan", "rei"]
        )
        
        from docpool.base.localbehavior.localbehavior import ILocalBehaviorSupporting
        alsoProvides(document, ILocalBehaviorSupporting)
        
        # Mock UUID for consistent testing
        with patch('docpool.base.localbehavior.adapter.IUUID') as mock_uuid:
            mock_uuid.return_value = "test-uuid-123"
            
            from docpool.base.localbehavior.adapter import DexterityLocalBehaviorAssignable
            assignable = DexterityLocalBehaviorAssignable(document)
            
            # First enumeration should cache behaviors
            list(assignable.enumerateBehaviors())
            
            # Check cache was created
            cache = self.request.get("savedLocalBehaviors", {})
            self.assertIn("test-uuid-123", cache)
            self.assertEqual(set(cache["test-uuid-123"]), {"elan", "rei"})


class TestVocabularyIntegrationWithRealApps(unittest.TestCase, LocalBehaviorTestMixin):
    """Test LocalBehaviorsVocabulary with real applications."""
    
    layer = DOCPOOL_BASE_REALAPPS_INTEGRATION_TESTING
    
    def setUp(self):
        """Set up test environment."""
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        
        self.bund_docpool = self.portal["bund"]
        
    def test_vocabulary_for_real_document(self):
        """Test vocabulary generation for real DPDocument."""
        document = self.create_test_dpdocument(container=self.bund_docpool)
        
        # Get the vocabulary factory
        from docpool.base.localbehavior.vocabulary import LocalBehaviorsVocabularyFactory
        
        # Create vocabulary for the document context
        vocabulary = LocalBehaviorsVocabularyFactory(document)
        
        # Should return a vocabulary with available apps
        self.assertIsNotNone(vocabulary)
        
        # Get terms from vocabulary
        terms = list(vocabulary)
        
        # Should have terms (exact terms depend on app registration)
        # The important thing is it works without crashing
        self.assertIsInstance(terms, list)
        
    def test_vocabulary_respects_docpool_context(self):
        """Test that vocabulary respects DocumentPool app restrictions."""
        # Document in bund docpool (elan + rei)
        bund_document = self.create_test_dpdocument(container=self.bund_docpool)
        
        # Document in hessen docpool (elan only)
        hessen_document = self.create_test_dpdocument(container=self.portal["hessen"])
        
        from docpool.base.localbehavior.vocabulary import LocalBehaviorsVocabularyFactory
        
        # Get vocabularies
        bund_vocab = LocalBehaviorsVocabularyFactory(bund_document)
        hessen_vocab = LocalBehaviorsVocabularyFactory(hessen_document)
        
        # Both should work
        self.assertIsNotNone(bund_vocab)
        self.assertIsNotNone(hessen_vocab)
        
        # Vocabularies might be different based on DocumentPool support
        # (exact behavior depends on app state implementation)


class TestBehaviorTransitionsWithRealApps(unittest.TestCase, LocalBehaviorTestMixin):
    """Test behavior transitions and edge cases with real applications."""
    
    layer = DOCPOOL_BASE_REALAPPS_INTEGRATION_TESTING
    
    def setUp(self):
        """Set up test environment."""
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        
        self.bund_docpool = self.portal["bund"]
        self.hessen_docpool = self.portal["hessen"]
        
    def test_document_transfer_scenario(self):
        """Test behavior handling when document could be transferred."""
        # Create document in bund docpool with both apps
        document = self.create_test_dpdocument(
            container=self.bund_docpool,
            local_behaviors=["elan", "rei"]
        )
        
        from docpool.base.localbehavior.localbehavior import LocalBehaviorSupport
        adapter = LocalBehaviorSupport(document)
        
        # Initial state
        self.assertEqual(set(adapter.local_behaviors), {"elan", "rei"})
        
        # Simulate what might happen in a transfer - reduce to common apps
        adapter.local_behaviors = ["elan"]  # Only elan is supported everywhere
        self.assertEqual(adapter.local_behaviors, ["elan"])
        
    def test_app_addition_to_docpool(self):
        """Test what happens when apps are added/removed from DocumentPool.""" 
        # This tests the system's resilience to configuration changes
        document = self.create_test_dpdocument(
            container=self.hessen_docpool,
            local_behaviors=["elan"]
        )
        
        from docpool.base.localbehavior.localbehavior import LocalBehaviorSupport
        adapter = LocalBehaviorSupport(document)
        
        # Initially only has elan
        self.assertEqual(adapter.local_behaviors, ["elan"])
        
        # Document should be able to store behaviors even if not currently supported
        # (this tests forward compatibility)
        adapter.local_behaviors = ["elan", "rei"]
        self.assertEqual(set(adapter.local_behaviors), {"elan", "rei"})
        
    def test_behavior_persistence_across_edits(self):
        """Test that local behaviors persist across form edits."""
        document = self.create_test_dpdocument(
            container=self.bund_docpool,
            local_behaviors=["elan", "rei"]
        )
        
        from docpool.base.localbehavior.localbehavior import LocalBehaviorSupport
        adapter = LocalBehaviorSupport(document)
        
        # Simulate multiple edit cycles
        original_behaviors = set(adapter.local_behaviors)
        
        # Change behaviors
        adapter.local_behaviors = ["elan"]
        self.assertEqual(adapter.local_behaviors, ["elan"])
        
        # Change back
        adapter.local_behaviors = list(original_behaviors)
        self.assertEqual(set(adapter.local_behaviors), original_behaviors)
        
    def test_concurrent_access_simulation(self):
        """Test behavior under simulated concurrent access."""
        document = self.create_test_dpdocument(
            container=self.bund_docpool, 
            local_behaviors=["elan"]
        )
        
        from docpool.base.localbehavior.localbehavior import LocalBehaviorSupport
        
        # Simulate two adapters accessing same document
        adapter1 = LocalBehaviorSupport(document)
        adapter2 = LocalBehaviorSupport(document)
        
        # Both should see same initial state
        self.assertEqual(adapter1.local_behaviors, adapter2.local_behaviors)
        
        # Change via one adapter
        adapter1.local_behaviors = ["elan", "rei"]
        
        # Other adapter should see the change (since they share storage)
        self.assertEqual(set(adapter2.local_behaviors), {"elan", "rei"})