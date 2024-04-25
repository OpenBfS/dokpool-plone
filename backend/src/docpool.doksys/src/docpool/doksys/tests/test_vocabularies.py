from docpool.doksys import _
from docpool.doksys.testing import DOCPOOL_DOKSYS_INTEGRATION_TESTING  # noqa
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.interfaces import IVocabularyTokenized

import unittest


class TestVocabularies(unittest.TestCase):
    layer = DOCPOOL_DOKSYS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_vocab_network_operators(self):
        vocab_name = "docpool.doksys.NetworkOperators"
        factory = getUtility(IVocabularyFactory, vocab_name)
        self.assertTrue(IVocabularyFactory.providedBy(factory))

        vocabulary = factory(self.portal)
        self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))
        self.assertEqual(
            vocabulary.getTerm("Schleswig-Holstein").title, _("Schleswig-Holstein")
        )

    def test_all_vocabularies(self):
        vocabularies = [
            "docpool.doksys.NetworkOperators",
            "docpool.doksys.Dom",
            "docpool.doksys.LegalBase",
            "docpool.doksys.MeasuringProgram",
            "docpool.doksys.Purpose",
            "docpool.doksys.Status",
            "docpool.doksys.OperationMode",
            "docpool.doksys.DataType",
            "docpool.doksys.SampleType",
            "docpool.doksys.MeasurementCategory",
            "docpool.doksys.Duration",
            "docpool.doksys.InfoType",
            "docpool.doksys.Area",
        ]
        for name in vocabularies:
            factory = getUtility(IVocabularyFactory, name)
            self.assertTrue(IVocabularyFactory.providedBy(factory))
            vocabulary = factory(self.portal)
            self.assertTrue(IVocabularyTokenized.providedBy(vocabulary))
