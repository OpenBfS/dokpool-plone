# -*- coding: utf-8 -*-
from docpool.event.testing import DOCPOOL_EVENT_INTEGRATION_TESTING
from plone.dexterity.interfaces import IDexterityFTI
from plone import api

import unittest


class TestEvent(unittest.TestCase):

    layer = DOCPOOL_EVENT_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_types_available(self):
        portal_types = api.portal.get_tool('portal_types')
        self.assertTrue(IDexterityFTI.providedBy(portal_types['DPEvent'])
        self.assertTrue(IDexterityFTI.providedBy(portal_types['DPEvents'])
        self.assertTrue(IDexterityFTI.providedBy(portal_types['DPNetwork'])
        self.assertTrue(IDexterityFTI.providedBy(portal_types['DPNuclearPowerStation'])
