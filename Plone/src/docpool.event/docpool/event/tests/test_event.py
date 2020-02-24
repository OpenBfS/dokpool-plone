# -*- coding: utf-8 -*-
from docpool.event.testing import DOCPOOL_EVENT_FUNCTIONAL_TESTING
from plone.dexterity.interfaces import IDexterityFTI
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class TestEvent(unittest.TestCase):

    layer = DOCPOOL_EVENT_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_types_available(self):
        portal_types = api.portal.get_tool('portal_types')
        self.assertTrue(IDexterityFTI.providedBy(portal_types['DPEvent']))
        self.assertTrue(IDexterityFTI.providedBy(portal_types['DPEvents']))
        self.assertTrue(IDexterityFTI.providedBy(portal_types['DPNetwork']))
        self.assertTrue(IDexterityFTI.providedBy(portal_types['DPNuclearPowerStation']))

    def test_add_event(self):
        docpool = self.portal['test_docpool']
        container = docpool['contentconfig']['scen']
        event = api.content.create(
            container=container,
            type='DPEvent',
            id='test_event',
            title=u'Test Event',
            )
        self.assertTrue(event.restrictedTraverse('@@view')())
        self.assertTrue(event.restrictedTraverse('@@edit')())

    def test_removal_keeps_working_for_arbitrary_dpevents(self):
        docpool = self.portal['test_docpool']
        container = docpool['contentconfig']['scen']
        event = api.content.create(
            container=container,
            type='DPEvent',
            id='test_event',
            title=u'Test Event',
            )
        try:
            api.content.delete(event)
        except Exception as e:
            self.fail(str(e))

    def test_removal_prevented_for_routinemode_dpevent(self):
        docpool = self.portal['test_docpool']
        container = docpool['contentconfig']['scen']
        event = container['routinemode']
        with self.assertRaises(RuntimeError):
            api.content.delete(event)

    def test_journals_for_event(self):
        docpool = self.portal['test_docpool']
        container = docpool['contentconfig']['scen']
        event = api.content.create(
            container=container,
            type='DPEvent',
            id='test_event',
            title=u'Test Event',
            )
        # check that 4 journals were added
        self.assertEqual(
            event.keys(),
            ['journal1', 'journal2', 'journal3', 'journal4'])
        self.assertEqual(
            [i.title for i in event.contentValues()],
            [u'Einsatztagebuch BfS', u'Einsatztagebuch RLZ', u'Einsatztagebuch SSK', u'Einsatztagebuch Messdienste'])

        # check the local roles for each journal
        self.assertEqual(
            event.journal1.get_local_roles(),
            (('test_docpool_Journal1_Editors', ('JournalEditor',)), ('test_docpool_Journal1_Readers', ('JournalReader',)), ('test_user_1_', ('Owner',))),
        )
        self.assertEqual(
            event.journal2.get_local_roles(),
            (('test_docpool_Journal2_Editors', ('JournalEditor',)), ('test_docpool_Journal2_Readers', ('JournalReader',)), ('test_user_1_', ('Owner',))),
        )
        self.assertEqual(
            event.journal3.get_local_roles(),
            (('test_docpool_Journal3_Editors', ('JournalEditor',)), ('test_docpool_Journal3_Readers', ('JournalReader',)), ('test_user_1_', ('Owner',))),
        )
        self.assertEqual(
            event.journal4.get_local_roles(),
            (('test_docpool_Journal4_Editors', ('JournalEditor',)), ('test_docpool_Journal4_Readers', ('JournalReader',)), ('test_user_1_', ('Owner',))),
        )

        # Check that 2 groups each for up to 5 journals actually exist
        self.assertTrue(api.group.get('test_docpool_Journal1_Readers'))
        self.assertTrue(api.group.get('test_docpool_Journal2_Readers'))
        self.assertTrue(api.group.get('test_docpool_Journal3_Readers'))
        self.assertTrue(api.group.get('test_docpool_Journal4_Readers'))
        self.assertTrue(api.group.get('test_docpool_Journal5_Readers'))
        self.assertIsNone(api.group.get('test_docpool_Journal6_Readers'))

        self.assertTrue(api.group.get('test_docpool_Journal1_Editors'))
        self.assertTrue(api.group.get('test_docpool_Journal2_Editors'))
        self.assertTrue(api.group.get('test_docpool_Journal3_Editors'))
        self.assertTrue(api.group.get('test_docpool_Journal4_Editors'))
        self.assertTrue(api.group.get('test_docpool_Journal5_Editors'))
        self.assertIsNone(api.group.get('test_docpool_Journal6_Editors'))

        # check that permissions are as defined in dp_journal_workflow
        self.assertEqual(
            event.journal1._View_Permission,
            ('Manager', 'Owner', 'ContentAdmin', 'Site Administrator', 'DocPoolAdmin', 'EventEditor', 'JournalEditor', 'JournalReader'))
        self.assertEqual(
            event.journal1._Modify_portal_content_Permission,
            ('Manager', 'Owner', 'ContentAdmin', 'Site Administrator', 'DocPoolAdmin', 'EventEditor', 'JournalEditor'))

