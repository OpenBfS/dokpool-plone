"""Setup tests for this package."""

from docpool.rei.testing import DOCPOOL_REI_INTEGRATION_TESTING
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

import unittest


class TestVocabularies(unittest.TestCase):
    """Test that docpool.rei is properly installed."""

    layer = DOCPOOL_REI_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]

    def test_authority_vocabulary(self):
        factory = getUtility(
            IVocabularyFactory,
            name="docpool.rei.vocabularies.AuthorityVocabulary",
            context=None,
        )
        self.assertTrue(IVocabularyFactory.providedBy(factory))
        voc = factory()
        self.assertEqual(len(voc), 18, msg="There should be 18 Authorities in the vocabulary")
        self.assertIn("de_hh", voc.by_token)
