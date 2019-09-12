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
