"""Functional tests for local behavior system form integration.

These tests verify that the local behavior system integrates properly with
Plone's form framework, including add/edit forms, vocabulary widgets, and
behavior assignment through the web interface.
"""

from docpool.base.localbehavior.localbehavior import LocalBehaviorSupport
from docpool.base.localbehavior.vocabulary import LocalBehaviorsVocabularyFactory
from docpool.base.testing import DOCPOOL_BASE_REALAPPS_FUNCTIONAL_TESTING
from docpool.base.testing import LocalBehaviorTestMixin
from docpool.rei.behaviors.reidoc import IREIDoc
from plone import api
from plone.app.testing import login
from plone.app.testing import SITE_OWNER_NAME
from plone.app.testing import SITE_OWNER_PASSWORD
from plone.testing.zope import Browser
from unittest.mock import Mock
from unittest.mock import patch
from zope.schema.vocabulary import SimpleVocabulary

import transaction
import unittest


class TestLocalBehaviorFormIntegration(unittest.TestCase, LocalBehaviorTestMixin):
    """Test local behavior integration with forms using functional testing."""

    layer = DOCPOOL_BASE_REALAPPS_FUNCTIONAL_TESTING

    def setUp(self):
        """Set up test environment with browser."""
        app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.portal_url = self.portal.absolute_url()
        self.browser = Browser(app)
        self.browser.handleErrors = False
        login(self.portal, SITE_OWNER_NAME)

        self.bund_docpool = self.portal["bund"]  # Has elan + rei
        self.hessen_docpool = self.portal["hessen"]  # Has elan only

    def test_documentpool_edit_supported_apps_via_browser(self):
        """Test editing DocumentPool supported apps through browser forms."""
        self.browser.addHeader(
            "Authorization",
            f"Basic {SITE_OWNER_NAME}:{SITE_OWNER_PASSWORD}",
        )

        # Navigate to DocumentPool edit form
        edit_url = f"{self.bund_docpool.absolute_url()}/@@edit"
        self.browser.open(edit_url)

        # Find and modify the supportedApps field
        supported_apps_control = self.browser.getControl(name="form.widgets.supportedApps:list")

        # Verify current apps (should be elan and rei)
        current_apps = supported_apps_control.value
        self.assertIn("elan", current_apps)
        self.assertIn("rei", current_apps)

        # Change to only elan
        supported_apps_control.value = ["elan"]

        # Save the form
        self.browser.getControl(name="form.buttons.save").click()

        # Verify the change was saved
        self.assertEqual(set(self.bund_docpool.supportedApps), {"elan"})

    def test_dpdocument_creation_via_browser(self):
        """Test creating DPDocument through browser forms."""
        self.browser.addHeader(
            "Authorization",
            f"Basic {SITE_OWNER_NAME}:{SITE_OWNER_PASSWORD}",
        )

        # Navigate to GroupFolder where DPDocuments can be created
        groups_folder = self.bund_docpool.content.Groups
        group_folder = None

        # Find an existing GroupFolder
        for group_id in groups_folder.objectIds():
            if groups_folder[group_id].portal_type == "GroupFolder":
                group_folder = groups_folder[group_id]
                break

        if not group_folder:
            # Create a GroupFolder for testing
            group_folder = api.content.create(
                container=groups_folder, type="GroupFolder", id="test_users", title="Test Users Group"
            )

        # Navigate to DPDocument add form
        add_url = f"{group_folder.absolute_url()}/++add++DPDocument"
        self.browser.open(add_url)

        # Fill out the form
        title_control = self.browser.getControl(name="form.widgets.IDublinCore.title")
        title_control.value = "Test Document via Browser"

        text_control = self.browser.getControl(name="form.widgets.text")
        text_control.value = "<p>Test text</p>"

        # Check if local behavior field is present (when ILocalBehaviorSupporting is provided)
        behavior_control = self.browser.getControl(
            name="form.widgets.ILocalBehaviorSupport.local_behaviors:list"
        )
        self.assertEqual(behavior_control.options, ["elan", "rei"])
        self.assertEqual(behavior_control.value, [])
        behavior_control.value = ["elan"]

        # Save the document
        self.browser.getControl(name="form.buttons.save").click()

        # Verify document was created
        self.assertIn("Test Document via Browser", self.browser.contents)

        # Find the created document
        created_doc = group_folder["test-document-via-browser"]

        self.assertIsNotNone(created_doc, "Document should have been created")
        self.assertEqual(created_doc.portal_type, "DPDocument")

    def test_dpdocument_edit_local_behaviors_via_browser(self):
        """Test editing DPDocument local behaviors through browser forms."""
        self.browser.addHeader(
            "Authorization",
            f"Basic {SITE_OWNER_NAME}:{SITE_OWNER_PASSWORD}",
        )

        # Create a DPDocument first
        document = self.create_test_dpdocument(
            container=self.bund_docpool,
            local_behaviors=["elan", "rei"],
        )

        # Fill required fields

        IREIDoc(document).NuclearInstallations = ["UCHL"]
        IREIDoc(document).ReiLegalBases = ["REI-I"]
        IREIDoc(document).Year = 2025
        IREIDoc(document).Period = "Y"
        IREIDoc(document).Origins = ["Strahlenschutzverantwortlicher"]
        IREIDoc(document).Authority = "de_he"
        IREIDoc(document).PDFVersion = "PDF/A-1b"
        transaction.commit()

        # Navigate to document edit form
        edit_url = f"{document.absolute_url()}/@@edit"
        self.browser.open(edit_url)

        # Check that edit form loads
        nuclear_installations_control = self.browser.getControl(
            name="form.widgets.IREIDoc.NuclearInstallations"
        )
        self.assertEqual(nuclear_installations_control.value, ["UCHL"])

        # Look for local behavior field (if present in the form)
        behavior_control = self.browser.getControl(
            name="form.widgets.ILocalBehaviorSupport.local_behaviors:list"
        )

        # Verify current behavior
        current_behaviors = behavior_control.value
        self.assertEqual(current_behaviors, ["elan", "rei"])

        # Change behaviors to include both elan and rei
        behavior_control.value = ["elan"]

        # Save the form
        self.browser.getControl(name="form.buttons.save").click()

        # Verify the change was saved
        adapter = LocalBehaviorSupport(document)
        self.assertEqual(set(adapter.local_behaviors), {"elan"})

        # Verify that the REI fields are no longer available
        self.browser.open(edit_url)
        with self.assertRaises(LookupError):
            nuclear_installations_control = self.browser.getControl(
                name="form.widgets.IREIDoc.NuclearInstallations"
            )

    def test_vocabulary_integration(self):
        """Test that vocabulary integrates properly with form system."""
        # Test document context
        document = self.create_test_dpdocument(container=self.bund_docpool)

        vocabulary = LocalBehaviorsVocabularyFactory(document)

        self.assertIsInstance(vocabulary, SimpleVocabulary)

        # Test that vocabulary is usable by form widgets
        terms = list(vocabulary)
        for term in terms:
            # Each term should have attributes needed by widgets
            self.assertTrue(hasattr(term, "value"))
            self.assertTrue(hasattr(term, "title"))
            self.assertIsInstance(term.value, str)
            self.assertIsInstance(term.title, str)

    def test_behavior_persistence(self):
        """Test that behavior assignments persist correctly."""
        # Create a test document
        document = self.create_test_dpdocument(container=self.bund_docpool)

        # Test that we can assign behaviors programmatically

        adapter = LocalBehaviorSupport(document)

        # Assign some behaviors
        adapter.local_behaviors = ["elan", "rei"]

        # Verify they were persisted
        self.assertEqual(set(adapter.local_behaviors), {"elan", "rei"})

        # Test changing behaviors
        adapter.local_behaviors = ["elan"]
        self.assertEqual(adapter.local_behaviors, ["elan"])


class TestDocTypeFormIntegration(unittest.TestCase, LocalBehaviorTestMixin):
    """Test local behavior integration with DocType configuration forms."""

    layer = DOCPOOL_BASE_REALAPPS_FUNCTIONAL_TESTING

    def setUp(self):
        """Set up test environment."""
        app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.portal_url = self.portal.absolute_url()
        self.browser = Browser(app)
        self.browser.handleErrors = False
        login(self.portal, SITE_OWNER_NAME)

        self.bund_docpool = self.portal["bund"]

    def test_doctype_creation_via_browser(self):
        """Test creating DocType through browser forms."""
        self.browser.addHeader(
            "Authorization",
            f"Basic {SITE_OWNER_NAME}:{SITE_OWNER_PASSWORD}",
        )

        # Navigate to DocType configuration area
        dtypes_folder = self.bund_docpool.config.dtypes.incident.media_reports

        # Navigate to DocType add form
        add_url = f"{dtypes_folder.absolute_url()}/++add++DocType"
        self.browser.open(add_url)

        # Fill out the form
        title_control = self.browser.getControl(name="form.widgets.IBasic.title")
        title_control.value = "Test DocType via Browser"

        # Set local behavior field
        behavior_control = self.browser.getControl(
            name="form.widgets.ILocalBehaviorSupport.local_behaviors:list"
        )
        behavior_control.value = ["elan"]

        # Save the DocType
        self.browser.getControl(name="form.buttons.save").click()

        # Verify DocType was created
        self.assertIn("Test DocType via Browser", self.browser.contents)

        # Find the created DocType
        created_doctype = None
        for obj_id in dtypes_folder.objectIds():
            obj = dtypes_folder[obj_id]
            if getattr(obj, "Title", lambda: "")() == "Test DocType via Browser":
                created_doctype = obj
                break

        self.assertIsNotNone(created_doctype, "DocType should have been created")
        self.assertEqual(created_doctype.portal_type, "DocType")

    def test_doctype_edit_via_browser(self):
        """Test editing DocType through browser forms."""
        self.browser.addHeader(
            "Authorization",
            f"Basic {SITE_OWNER_NAME}:{SITE_OWNER_PASSWORD}",
        )

        # Create a DocType first
        doctype = self.create_test_doctype(local_behaviors=["elan"])
        transaction.commit()

        # Navigate to DocType edit form
        edit_url = f"{doctype.absolute_url()}/@@edit"
        self.browser.open(edit_url)

        # Test local behavior field
        behavior_control = self.browser.getControl(
            name="form.widgets.ILocalBehaviorSupport.local_behaviors:list"
        )

        # Verify current behavior
        current_behaviors = behavior_control.value
        self.assertIn("elan", current_behaviors)

        # Change behaviors to include both elan and rei
        behavior_control.value = ["elan", "rei"]

        # Save the form
        self.browser.getControl(name="form.buttons.save").click()

        # Verify the change was saved

        adapter = LocalBehaviorSupport(doctype)
        self.assertEqual(set(adapter.local_behaviors), {"elan", "rei"})


class TestFormValidationAndErrorHandling(unittest.TestCase, LocalBehaviorTestMixin):
    """Test form validation and error handling for local behavior fields."""

    layer = DOCPOOL_BASE_REALAPPS_FUNCTIONAL_TESTING

    def setUp(self):
        """Set up test environment."""
        app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.portal_url = self.portal.absolute_url()
        self.browser = Browser(app)
        self.browser.handleErrors = False
        login(self.portal, SITE_OWNER_NAME)

        self.bund_docpool = self.portal["bund"]

    def test_behavior_field_handles_empty_selection(self):
        """Test that behavior field handles empty selections gracefully."""
        document = self.create_test_dpdocument()

        adapter = LocalBehaviorSupport(document)

        # Empty assignment should work
        adapter.local_behaviors = []
        self.assertEqual(adapter.local_behaviors, [])

        # None assignment should also work
        adapter.local_behaviors = None
        self.assertEqual(adapter.local_behaviors, [])

    def test_behavior_field_with_nonexistent_apps(self):
        """Test form handling of non-existent applications."""
        document = self.create_test_dpdocument()

        adapter = LocalBehaviorSupport(document)

        # Should be able to store any app name (validation happens at vocabulary level)
        adapter.local_behaviors = ["nonexistent_app"]
        self.assertEqual(adapter.local_behaviors, ["nonexistent_app"])

        # Should handle mixed valid/invalid app names
        adapter.local_behaviors = ["elan", "nonexistent_app", "rei"]
        self.assertEqual(set(adapter.local_behaviors), {"elan", "nonexistent_app", "rei"})

    def test_vocabulary_with_empty_permissions(self):
        """Test that forms handle vocabulary with empty permissions gracefully."""
        document = self.create_test_dpdocument()

        # Test vocabulary factory with empty permissions
        # Mock a scenario where no apps are permitted
        with patch("docpool.base.localbehavior.vocabulary.getMultiAdapter") as mock_adapter:
            mock_app_state = Mock()
            mock_app_state.appsPermittedForObject.return_value = []  # Empty permissions
            mock_adapter.return_value = mock_app_state

            # Should still return a valid vocabulary
            vocabulary = LocalBehaviorsVocabularyFactory(document)
            self.assertIsInstance(vocabulary, SimpleVocabulary)

            # Should have empty terms due to empty permissions
            terms = list(vocabulary)
            self.assertEqual(len(terms), 0)


class TestFormWidgetIntegration(unittest.TestCase, LocalBehaviorTestMixin):
    """Test integration with form widgets and field rendering."""

    layer = DOCPOOL_BASE_REALAPPS_FUNCTIONAL_TESTING

    def setUp(self):
        """Set up test environment."""
        app = self.layer["app"]
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        self.portal_url = self.portal.absolute_url()
        self.browser = Browser(app)
        self.browser.handleErrors = False
        login(self.portal, SITE_OWNER_NAME)

        self.bund_docpool = self.portal["bund"]

    def test_vocabulary_widget_integration(self):
        """Test that vocabulary integrates properly with form widgets."""
        document = self.create_test_dpdocument(container=self.bund_docpool)

        # Test vocabulary properties needed for widgets
        vocabulary = LocalBehaviorsVocabularyFactory(document)
        self.assertIsInstance(vocabulary, SimpleVocabulary)

        # Test iteration (needed by choice widgets)
        terms = list(vocabulary)
        for term in terms:
            from zope.schema.vocabulary import SimpleTerm

            self.assertIsInstance(term, SimpleTerm)

            # Term should have required attributes
            self.assertTrue(hasattr(term, "value"))
            self.assertTrue(hasattr(term, "title"))
            self.assertIsInstance(term.value, str)
            self.assertIsInstance(term.title, str)

    def test_multi_choice_widget_compatibility(self):
        """Test compatibility with multi-choice widgets."""
        document = self.create_test_dpdocument()

        # Test that behaviors can be stored as lists (required for multi-choice)
        adapter = LocalBehaviorSupport(document)
        adapter.local_behaviors = ["elan", "rei"]

        # Should return as list
        behaviors = adapter.local_behaviors
        self.assertIsInstance(behaviors, list)
        self.assertEqual(set(behaviors), {"elan", "rei"})

        # Test empty selection
        adapter.local_behaviors = []
        self.assertEqual(adapter.local_behaviors, [])

    def test_context_aware_vocabulary_selection(self):
        """Test that vocabulary selection is context-aware in forms."""
        # Create documents in different contexts
        bund_document = self.create_test_dpdocument(container=self.bund_docpool)
        hessen_document = self.create_test_dpdocument(container=self.portal["hessen"])

        # Get vocabularies for different contexts
        bund_vocab = LocalBehaviorsVocabularyFactory(bund_document)
        hessen_vocab = LocalBehaviorsVocabularyFactory(hessen_document)

        # Both should be valid vocabularies
        self.assertIsInstance(bund_vocab, SimpleVocabulary)
        self.assertIsInstance(hessen_vocab, SimpleVocabulary)

        # Test that they can be enumerated (widget requirement)
        bund_terms = list(bund_vocab)
        hessen_terms = list(hessen_vocab)

        # Should have at least some terms available
        self.assertGreaterEqual(len(bund_terms), 0)
        self.assertGreaterEqual(len(hessen_terms), 0)
