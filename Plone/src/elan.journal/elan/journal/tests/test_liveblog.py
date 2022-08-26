from elan.journal.interfaces import IJournal
from elan.journal.testing import INTEGRATION_TESTING
from elan.journal.tests.utils import _create_journalentries
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import createObject
from zope.component import queryUtility

import unittest


class ContentTypeTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        with api.env.adopt_roles(["Manager"]):
            self.journal = api.content.create(self.portal, "Journal", "journal")

    def test_adding(self):
        self.assertTrue(IJournal.providedBy(self.journal))

    def test_fti(self):
        fti = queryUtility(IDexterityFTI, name="Journal")
        self.assertIsNotNone(fti)

    def test_schema(self):
        fti = queryUtility(IDexterityFTI, name="Journal")
        schema = fti.lookupSchema()
        self.assertEqual(IJournal, schema)

    def test_factory(self):
        fti = queryUtility(IDexterityFTI, name="Journal")
        factory = fti.factory
        new_object = createObject(factory)
        self.assertTrue(IJournal.providedBy(new_object))

    def test_exclude_from_navigation_behavior(self):
        from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation

        self.assertTrue(IExcludeFromNavigation.providedBy(self.journal))

    def test_content_types_constrains(self):
        allowed_types = [t.getId() for t in self.journal.allowedContentTypes()]
        self.assertListEqual(allowed_types, ["Image"])

    def test_get_journalentries(self):
        self.assertEqual(len(self.journal.get_journalentries()), 0)
        _create_journalentries(self.journal, 10)
        self.assertEqual(len(self.journal.get_journalentries()), 10)
