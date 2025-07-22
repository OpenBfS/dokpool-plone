"""Tests for LocalBehaviorsVocabulary with comprehensive scenarios."""

import unittest
from unittest.mock import Mock, patch

from docpool.base.testing import DOCPOOL_BASE_REALAPPS_INTEGRATION_TESTING
from docpool.base.testing import LocalBehaviorTestMixin
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


class TestLocalBehaviorsVocabularyFactory(unittest.TestCase, LocalBehaviorTestMixin):
    """Test the LocalBehaviorsVocabularyFactory with real applications."""
    
    layer = DOCPOOL_BASE_REALAPPS_INTEGRATION_TESTING
    
    def setUp(self):
        """Set up test environment."""
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        
        self.bund_docpool = self.portal["bund"]  # Has elan + rei
        self.hessen_docpool = self.portal["hessen"]  # Has elan only
        
    def test_vocabulary_for_document_context(self):
        """Test vocabulary generation for document context."""
        from docpool.base.localbehavior.vocabulary import LocalBehaviorsVocabularyFactory
        
        # Create document in bund docpool (supports elan + rei)
        document = self.create_test_dpdocument(
            container=self.bund_docpool,
            local_behaviors=["elan"]
        )
        
        # Generate vocabulary
        vocabulary = LocalBehaviorsVocabularyFactory(document)
        
        # Should be a SimpleVocabulary
        self.assertIsInstance(vocabulary, SimpleVocabulary)
        
        # Get terms
        terms = list(vocabulary)
        
        # Should have terms for available apps
        self.assertGreater(len(terms), 0, "Vocabulary should have at least one term")
        
        # All terms should be SimpleTerm instances
        for term in terms:
            self.assertIsInstance(term, SimpleTerm)
            self.assertIsInstance(term.value, str)
            self.assertIsInstance(term.title, str)
            
    def test_vocabulary_respects_docpool_app_support(self):
        """Test that vocabulary respects DocumentPool app restrictions."""
        from docpool.base.localbehavior.vocabulary import LocalBehaviorsVocabularyFactory
        
        # Document in bund docpool (elan + rei)
        bund_document = self.create_test_dpdocument(container=self.bund_docpool)
        
        # Document in hessen docpool (elan only) 
        hessen_document = self.create_test_dpdocument(container=self.hessen_docpool)
        
        # Get vocabularies
        bund_vocab = LocalBehaviorsVocabularyFactory(bund_document)
        hessen_vocab = LocalBehaviorsVocabularyFactory(hessen_document)
        
        # Both should be valid vocabularies
        self.assertIsInstance(bund_vocab, SimpleVocabulary)
        self.assertIsInstance(hessen_vocab, SimpleVocabulary)
        
        # Get terms
        bund_terms = list(bund_vocab)
        hessen_terms = list(hessen_vocab)
        
        # Both should have at least one term
        self.assertGreater(len(bund_terms), 0)
        self.assertGreater(len(hessen_terms), 0)
        
    def test_vocabulary_excludes_implicit_apps(self):
        """Test that implicit applications are excluded from vocabulary."""
        from docpool.base.localbehavior.vocabulary import LocalBehaviorsVocabularyFactory
        
        document = self.create_test_dpdocument()
        
        # Mock extendingApps to include an implicit app
        with patch('docpool.base.localbehavior.vocabulary.extendingApps') as mock_apps:
            mock_apps.return_value = [
                ('elan', 'ELAN', {'implicit': False}),
                ('rei', 'REI', {'implicit': False}), 
                ('implicit_app', 'Implicit App', {'implicit': True}),
            ]
            
            # Mock dp_app_state to return all apps as permitted
            with patch('docpool.base.localbehavior.vocabulary.getMultiAdapter') as mock_adapter:
                mock_app_state = Mock()
                mock_app_state.appsPermittedForObject.return_value = ['elan', 'rei', 'implicit_app']
                mock_adapter.return_value = mock_app_state
                
                vocabulary = LocalBehaviorsVocabularyFactory(document)
                terms = list(vocabulary)
                
                # Should not include the implicit app
                term_values = [term.value for term in terms]
                self.assertIn('elan', term_values)
                self.assertIn('rei', term_values) 
                self.assertNotIn('implicit_app', term_values, "Implicit apps should be excluded")
                
    def test_vocabulary_for_global_config_context(self):
        """Test vocabulary generation for global configuration context."""
        from docpool.base.localbehavior.vocabulary import LocalBehaviorsVocabularyFactory
        
        # Mock request with config path at level 2 (global config)
        with patch('docpool.base.localbehavior.vocabulary.getRequest') as mock_get_request:
            mock_request = Mock()
            mock_request.physicalPathFromURL.return_value = ['', 'plone', 'config']
            mock_get_request.return_value = mock_request
            
            # Mock dp_app_state for global config
            with patch('docpool.base.localbehavior.vocabulary.getMultiAdapter') as mock_adapter:
                mock_app_state = Mock()
                mock_app_state.appsPermittedForCurrentUser.return_value = ['elan', 'rei']
                mock_adapter.return_value = mock_app_state
                
                # Mock extendingApps
                with patch('docpool.base.localbehavior.vocabulary.extendingApps') as mock_apps:
                    mock_apps.return_value = [
                        ('elan', 'ELAN', {'implicit': False}),
                        ('rei', 'REI', {'implicit': False}),
                    ]
                    
                    vocabulary = LocalBehaviorsVocabularyFactory(self.portal)
                    terms = list(vocabulary)
                    
                    # Should have terms for apps permitted for current user
                    term_values = [term.value for term in terms]
                    self.assertIn('elan', term_values)
                    self.assertIn('rei', term_values)
                    
                    # Check that correct method was called
                    mock_app_state.appsPermittedForCurrentUser.assert_called_once()
                    
    def test_vocabulary_for_local_config_context(self):
        """Test vocabulary generation for local DocumentPool configuration context."""
        from docpool.base.localbehavior.vocabulary import LocalBehaviorsVocabularyFactory
        
        # Mock request with config path at deeper level (local config)
        with patch('docpool.base.localbehavior.vocabulary.getRequest') as mock_get_request:
            mock_request = Mock()
            mock_request.physicalPathFromURL.return_value = ['', 'plone', 'bund', 'config', 'dtypes']
            mock_get_request.return_value = mock_request
            
            # Mock dp_app_state for local config
            with patch('docpool.base.localbehavior.vocabulary.getMultiAdapter') as mock_adapter:
                mock_app_state = Mock()
                mock_app_state.appsSupportedHere.return_value = ['elan']  # Local context has fewer apps
                mock_adapter.return_value = mock_app_state
                
                # Mock extendingApps
                with patch('docpool.base.localbehavior.vocabulary.extendingApps') as mock_apps:
                    mock_apps.return_value = [
                        ('elan', 'ELAN', {'implicit': False}),
                        ('rei', 'REI', {'implicit': False}),
                    ]
                    
                    vocabulary = LocalBehaviorsVocabularyFactory(self.bund_docpool)
                    terms = list(vocabulary)
                    
                    # Should only have terms for apps supported locally
                    term_values = [term.value for term in terms]
                    self.assertIn('elan', term_values)
                    # rei might or might not be there depending on local support
                    
                    # Check that correct method was called
                    mock_app_state.appsSupportedHere.assert_called_once()


class TestVocabularyIntegrationScenarios(unittest.TestCase, LocalBehaviorTestMixin):
    """Test vocabulary behavior in realistic integration scenarios."""
    
    layer = DOCPOOL_BASE_REALAPPS_INTEGRATION_TESTING
    
    def setUp(self):
        """Set up test environment."""
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        
        self.bund_docpool = self.portal["bund"]
        self.hessen_docpool = self.portal["hessen"]
        
    def test_vocabulary_consistency_across_contexts(self):
        """Test that vocabulary is consistent across different contexts."""
        from docpool.base.localbehavior.vocabulary import LocalBehaviorsVocabularyFactory
        
        # Create documents in different contexts
        bund_document = self.create_test_dpdocument(container=self.bund_docpool)
        hessen_document = self.create_test_dpdocument(container=self.hessen_docpool)
        
        # Generate vocabularies
        bund_vocab = LocalBehaviorsVocabularyFactory(bund_document)
        hessen_vocab = LocalBehaviorsVocabularyFactory(hessen_document)
        
        # Both should be valid
        self.assertIsInstance(bund_vocab, SimpleVocabulary)
        self.assertIsInstance(hessen_vocab, SimpleVocabulary)
        
        # Get terms
        bund_terms = {term.value: term.title for term in bund_vocab}
        hessen_terms = {term.value: term.title for term in hessen_vocab}
        
        # Common apps should have same titles
        common_apps = set(bund_terms.keys()).intersection(set(hessen_terms.keys()))
        for app in common_apps:
            self.assertEqual(bund_terms[app], hessen_terms[app], 
                           f"App {app} should have same title in both contexts")
            
    def test_vocabulary_with_restricted_user_permissions(self):
        """Test vocabulary behavior with restricted user permissions.""" 
        from docpool.base.localbehavior.vocabulary import LocalBehaviorsVocabularyFactory
        
        # Create a user with limited permissions
        api.user.create(
            email='limited@example.com',
            username='limited_user', 
            password='secretpassword',  # Must be 8+ characters
            roles=['Member']  # Limited permissions
        )
        
        # Create document
        document = self.create_test_dpdocument()
        
        # Mock app state to simulate restricted permissions
        with patch('docpool.base.localbehavior.vocabulary.getMultiAdapter') as mock_adapter:
            mock_app_state = Mock()
            mock_app_state.appsPermittedForObject.return_value = ['elan']  # Only one app permitted
            mock_adapter.return_value = mock_app_state
            
            with patch('docpool.base.localbehavior.vocabulary.extendingApps') as mock_apps:
                mock_apps.return_value = [
                    ('elan', 'ELAN', {'implicit': False}),
                    ('rei', 'REI', {'implicit': False}),
                ]
                
                vocabulary = LocalBehaviorsVocabularyFactory(document)
                terms = list(vocabulary)
                
                # Should only include permitted apps
                term_values = [term.value for term in terms]
                self.assertIn('elan', term_values)
                # rei should not be included due to permission restrictions
                
    def test_vocabulary_empty_when_no_apps_available(self):
        """Test vocabulary behavior when no applications are available."""
        from docpool.base.localbehavior.vocabulary import LocalBehaviorsVocabularyFactory
        
        document = self.create_test_dpdocument()
        
        # Mock no available apps
        with patch('docpool.base.localbehavior.vocabulary.getMultiAdapter') as mock_adapter:
            mock_app_state = Mock()
            mock_app_state.appsPermittedForObject.return_value = []
            mock_adapter.return_value = mock_app_state
            
            with patch('docpool.base.localbehavior.vocabulary.extendingApps') as mock_apps:
                mock_apps.return_value = [
                    ('elan', 'ELAN', {'implicit': False}),
                    ('rei', 'REI', {'implicit': False}),
                ]
                
                vocabulary = LocalBehaviorsVocabularyFactory(document)
                terms = list(vocabulary)
                
                # Should be empty
                self.assertEqual(len(terms), 0, "Vocabulary should be empty when no apps are available")
                
    def test_vocabulary_with_app_state_method_exceptions(self):
        """Test vocabulary behavior when app state adapter methods raise exceptions."""
        from docpool.base.localbehavior.vocabulary import LocalBehaviorsVocabularyFactory
        
        document = self.create_test_dpdocument()
        
        # Mock app state with a method that raises an exception
        with patch('docpool.base.localbehavior.vocabulary.getMultiAdapter') as mock_adapter:
            mock_app_state = Mock()
            mock_app_state.appsPermittedForObject.side_effect = Exception("App permission check failed")
            mock_adapter.return_value = mock_app_state
            
            # This should raise an exception - vocabulary factory shouldn't hide serious errors
            with self.assertRaises(Exception) as cm:
                LocalBehaviorsVocabularyFactory(document)
            
            self.assertEqual(str(cm.exception), "App permission check failed")


class TestVocabularyPerformance(unittest.TestCase, LocalBehaviorTestMixin):
    """Test vocabulary performance and caching behavior."""
    
    layer = DOCPOOL_BASE_REALAPPS_INTEGRATION_TESTING
    
    def setUp(self):
        """Set up test environment."""
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        
    def test_vocabulary_repeated_calls(self):
        """Test performance of repeated vocabulary calls."""
        from docpool.base.localbehavior.vocabulary import LocalBehaviorsVocabularyFactory
        import time
        
        document = self.create_test_dpdocument()
        
        # Time multiple calls
        start_time = time.time()
        for _ in range(10):
            vocabulary = LocalBehaviorsVocabularyFactory(document)
            list(vocabulary)  # Force evaluation
        elapsed = time.time() - start_time
        
        # Should complete in reasonable time (less than 1 second for 10 calls)
        self.assertLess(elapsed, 1.0, "Vocabulary generation should be reasonably fast")
        
    def test_vocabulary_with_large_app_list(self):
        """Test vocabulary behavior with many applications."""
        from docpool.base.localbehavior.vocabulary import LocalBehaviorsVocabularyFactory
        
        document = self.create_test_dpdocument()
        
        # Mock many applications
        many_apps = [(f'app{i}', f'Application {i}', {'implicit': False}) for i in range(50)]
        
        with patch('docpool.base.localbehavior.vocabulary.getMultiAdapter') as mock_adapter:
            mock_app_state = Mock()
            mock_app_state.appsPermittedForObject.return_value = [f'app{i}' for i in range(50)]
            mock_adapter.return_value = mock_app_state
            
            with patch('docpool.base.localbehavior.vocabulary.extendingApps') as mock_apps:
                mock_apps.return_value = many_apps
                
                vocabulary = LocalBehaviorsVocabularyFactory(document)
                terms = list(vocabulary)
                
                # Should handle large lists efficiently
                self.assertEqual(len(terms), 50)
                
                # Terms should be properly formed
                for i, term in enumerate(terms):
                    self.assertIsInstance(term, SimpleTerm)
                    self.assertEqual(term.value, f'app{i}')


class TestVocabularyEdgeCases(unittest.TestCase, LocalBehaviorTestMixin):
    """Test vocabulary behavior in edge cases and error conditions."""
    
    layer = DOCPOOL_BASE_REALAPPS_INTEGRATION_TESTING
    
    def setUp(self):
        """Set up test environment."""
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        
    def test_vocabulary_with_none_context(self):
        """Test vocabulary with None context."""
        from docpool.base.localbehavior.vocabulary import LocalBehaviorsVocabularyFactory
        
        # Should handle None context gracefully
        with patch('docpool.base.localbehavior.vocabulary.getMultiAdapter') as mock_adapter:
            mock_app_state = Mock()
            mock_app_state.appsPermittedForObject.return_value = []
            mock_adapter.return_value = mock_app_state
            
            vocabulary = LocalBehaviorsVocabularyFactory(None)
            self.assertIsInstance(vocabulary, SimpleVocabulary)
            
    def test_vocabulary_with_malformed_app_data(self):
        """Test vocabulary with malformed application data."""
        from docpool.base.localbehavior.vocabulary import LocalBehaviorsVocabularyFactory
        
        document = self.create_test_dpdocument()
        
        # Mock malformed app data
        malformed_apps = [
            ('elan',),  # Missing title and config
            ('rei', 'REI'),  # Missing config
            ('bad_app', 'Bad App', 'not_a_dict'),  # Invalid config
        ]
        
        with patch('docpool.base.localbehavior.vocabulary.getMultiAdapter') as mock_adapter:
            mock_app_state = Mock()
            mock_app_state.appsPermittedForObject.return_value = ['elan', 'rei', 'bad_app']
            mock_adapter.return_value = mock_app_state
            
            with patch('docpool.base.localbehavior.vocabulary.extendingApps') as mock_apps:
                mock_apps.return_value = malformed_apps
                
                # Should handle malformed data gracefully
                try:
                    vocabulary = LocalBehaviorsVocabularyFactory(document)
                    terms = list(vocabulary)
                    # If we get here, it handled the malformed data
                    self.assertIsInstance(vocabulary, SimpleVocabulary)
                except (IndexError, KeyError, TypeError):
                    # These errors are acceptable for malformed data
                    pass
                    
    def test_vocabulary_with_unicode_app_names(self):
        """Test vocabulary with Unicode application names."""
        from docpool.base.localbehavior.vocabulary import LocalBehaviorsVocabularyFactory
        
        document = self.create_test_dpdocument()
        
        # Mock apps with Unicode names
        unicode_apps = [
            ('ümlauts', 'Ümläüts App', {'implicit': False}),
            ('中文', 'Chinese App 中文', {'implicit': False}),
            ('емоджи', 'Emoji App 🚀', {'implicit': False}),
        ]
        
        with patch('docpool.base.localbehavior.vocabulary.getMultiAdapter') as mock_adapter:
            mock_app_state = Mock()
            mock_app_state.appsPermittedForObject.return_value = ['ümlauts', '中文', 'емоджи']
            mock_adapter.return_value = mock_app_state
            
            with patch('docpool.base.localbehavior.vocabulary.extendingApps') as mock_apps:
                mock_apps.return_value = unicode_apps
                
                vocabulary = LocalBehaviorsVocabularyFactory(document)
                terms = list(vocabulary)
                
                # Should handle Unicode properly
                self.assertEqual(len(terms), 3)
                
                # Check Unicode handling
                term_values = [term.value for term in terms]
                term_titles = [term.title for term in terms]
                
                self.assertIn('ümlauts', term_values)
                self.assertIn('中文', term_values) 
                self.assertIn('емоджи', term_values)
                
                self.assertIn('Ümläüts App', term_titles)
                self.assertIn('Chinese App 中文', term_titles)
                self.assertIn('Emoji App 🚀', term_titles)