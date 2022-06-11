from docpool.base.content.documentpool import APPLICATIONS_KEY
from docpool.doksys.testing import DOCPOOL_DOKSYS_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.events import EditFinishedEvent
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility
from zope.event import notify
from zope.schema.interfaces import IVocabularyFactory

import unittest


class TestSetup(unittest.TestCase):
    """Test that docpool.doksys is properly installed."""

    layer = DOCPOOL_DOKSYS_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_doksys_available(self):
        voc = getUtility(IVocabularyFactory, 'docpool.base.vocabularies.SelectableApps')
        self.assertTrue('doksys' in voc(None))
        docpool_without_doksys = api.content.create(
            container=self.portal,
            type='DocumentPool',
            id='test_doksys',
            title='Test Doksys',
            supportedApps=(),
            )
        docpool = api.content.create(
            container=self.portal,
            type='DocumentPool',
            id='test_docpool',
            title='Test Doksys',
            supportedApps=('doksys',),
            )
        self.assertIn('doksys', IAnnotations(docpool)[APPLICATIONS_KEY])
        self.assertNotIn('doksys', IAnnotations(docpool_without_doksys)[APPLICATIONS_KEY])
        self.assertEqual(docpool_without_doksys.contentIds(), ['content', 'config'])
        self.assertEqual(docpool.contentIds(), ['searches', 'content', 'config'])

    def test_doksys_install_method_run_on_edit(self):
        docpool = api.content.create(
            container=self.portal,
            type='DocumentPool',
            id='test_docpool',
            title='Test Doksys',
            supportedApps=(),
            )
        self.assertEqual(docpool.contentIds(), ['content', 'config'])
        docpool.supportedApps = ('doksys',)
        notify(EditFinishedEvent(docpool))
        self.assertEqual(docpool.contentIds(), ['searches', 'content', 'config'])
