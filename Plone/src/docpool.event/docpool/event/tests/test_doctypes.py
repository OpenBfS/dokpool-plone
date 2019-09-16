# -*- coding: utf-8 -*-
from docpool.event.testing import DOCPOOL_EVENT_FUNCTIONAL_TESTING
from plone import api
from plone.app.testing import login
from plone.app.testing import logout
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.dexterity.events import EditFinishedEvent
from zope.component import getUtility
from zope.event import notify
from zope.lifecycleevent import modified
from zope.schema.interfaces import IVocabularyFactory

import unittest


class TestDocTypes(unittest.TestCase):

    layer = DOCPOOL_EVENT_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_default_content(self):
        global_config = self.portal['config']
        global_contentconfig = self.portal['contentconfig']
        global_esd = self.portal['esd']
        self.assertEqual(global_config.portal_type, 'DPConfig')
        self.assertEqual(global_contentconfig.portal_type, 'ELANContentConfig')
        self.assertEqual(global_esd.portal_type, 'ELANCurrentSituation')

        global_dtypes = global_config['dtypes']
        self.assertEqual(
            global_dtypes.keys(),
            [
                'notification',
                'note',
                'eventinformation',
                'nppinformation',
                'weatherinformation',
                'trajectory',
                'rodosprojection',
                'stateprojection',
                'otherprojection',
                'gammadoserate',
                'gammadoserate_timeseries',
                'gammadoserate_mobile',
                'airactivity',
                'mresult_insitu',
                'groundcontamination',
                'mresult_feed',
                'mresult_food',
                'mresult_water',
                'mresult_other',
                'mresult_flight',
                'situationreport',
                'sitrep',
                'estimation',
                'instructions',
                'protectiveactions',
                'mediarelease',
                'insituinformation',
            ],
        )
        self.assertEqual(global_contentconfig.keys(), ['impressum', 'help'])
        self.assertEqual(
            global_esd.keys(),
            [
                'front-page',
                'incident',
                'meteorology',
                'dose-projections',
                'measurement-results',
                'current-situation',
                'information-of-the-public',
                'overview',
                'recent',
                'dashboard',
                'situationoverview',
            ],
        )

        from docpool.base.appregistry import selectableApps

        self.assertEqual([i[0] for i in selectableApps()], ['doksys', 'elan'])
        docpool = self.portal['test_docpool']

        self.assertEqual(
            docpool.keys(), ['esd', 'content', 'config', 'archive', 'contentconfig']
        )

        esd = docpool['esd']
        self.assertEqual(
            esd.keys(),
            [
                'front-page',
                'incident',
                'meteorology',
                'dose-projections',
                'measurement-results',
                'current-situation',
                'information-of-the-public',
                'overview',
                'recent',
                'dashboard',
                'situationoverview',
            ],
        )

        content = docpool['content']
        self.assertEqual(content.keys(), ['Transfers', 'Members', 'Groups'])

        config = docpool['config']
        self.assertEqual(config.keys(), ['dtypes'])

        dtypes = docpool['config']['dtypes']
        self.assertEqual(
            dtypes.keys(),
            [
                'notification',
                'note',
                'eventinformation',
                'nppinformation',
                'weatherinformation',
                'trajectory',
                'rodosprojection',
                'stateprojection',
                'otherprojection',
                'gammadoserate',
                'gammadoserate_timeseries',
                'gammadoserate_mobile',
                'airactivity',
                'mresult_insitu',
                'groundcontamination',
                'mresult_feed',
                'mresult_food',
                'mresult_water',
                'mresult_other',
                'mresult_flight',
                'situationreport',
                'sitrep',
                'estimation',
                'instructions',
                'protectiveactions',
                'mediarelease',
                'insituinformation',
            ],
        )

        archive = docpool['archive']
        self.assertEqual(archive.keys(), ['.wf_policy_config'])

        contentconfig = docpool['contentconfig']
        self.assertEqual(
            contentconfig.keys(), ['scen', 'ticker', 'impressum', 'dbconfig', 'irix']
        )

        notify(EditFinishedEvent(docpool))
        # trigger dpAdded method for enabled docpool-products
        # since only elan is active that doe not create new content

        self.assertEqual(
            docpool.keys(), ['esd', 'content', 'config', 'archive', 'contentconfig']
        )

        esd = docpool['esd']
        self.assertEqual(
            esd.keys(),
            [
                'front-page',
                'incident',
                'meteorology',
                'dose-projections',
                'measurement-results',
                'current-situation',
                'information-of-the-public',
                'overview',
                'recent',
                'dashboard',
                'situationoverview',
            ],
        )

        content = docpool['content']
        self.assertEqual(content.keys(), ['Transfers', 'Members', 'Groups'])

        config = docpool['config']
        self.assertEqual(config.keys(), ['dtypes'])

        dtypes = docpool['config']['dtypes']
        self.assertEqual(
            dtypes.keys(),
            [
                'notification',
                'note',
                'eventinformation',
                'nppinformation',
                'weatherinformation',
                'trajectory',
                'rodosprojection',
                'stateprojection',
                'otherprojection',
                'gammadoserate',
                'gammadoserate_timeseries',
                'gammadoserate_mobile',
                'airactivity',
                'mresult_insitu',
                'groundcontamination',
                'mresult_feed',
                'mresult_food',
                'mresult_water',
                'mresult_other',
                'mresult_flight',
                'situationreport',
                'sitrep',
                'estimation',
                'instructions',
                'protectiveactions',
                'mediarelease',
                'insituinformation',
            ],
        )

        archive = docpool['archive']
        self.assertEqual(archive.keys(), ['.wf_policy_config'])

        contentconfig = docpool['contentconfig']
        self.assertEqual(
            contentconfig.keys(), ['scen', 'ticker', 'impressum', 'dbconfig', 'irix']
        )

    def test_doctypes_change_event(self):
        docpool = self.portal['test_docpool']

        # check for available subtypes of DPDocument
        voc = getUtility(IVocabularyFactory, name='docpool.base.vocabularies.DocType')
        doctypes = voc(self.portal).by_value
        doctypes_ids = [i.id for i in doctypes]
        self.assertEqual(
            set(doctypes_ids),
            set(
                [
                    'notification',
                    'rodosprojection',
                    'mresult_flight',
                    'mediarelease',
                    'mresult_feed',
                    'protectiveactions',
                    'mresult_food',
                    'instructions',
                    'weatherinformation',
                    'mresult_insitu',
                    'mresult_water',
                    'airactivity',
                    'mresult_other',
                    'insituinformation',
                    'eventinformation',
                    'nppinformation',
                    'trajectory',
                    'gammadoserate_mobile',
                    'gammadoserate',
                    'gammadoserate_timeseries',
                    'otherprojection',
                    'groundcontamination',
                    'stateprojection',
                    'estimation',
                    'situationreport',
                    'sitrep',
                    'note',
                ]
            ),
        )

        # get the content-folder for a group to test with
        groups = docpool['content']['Groups']
        folder = groups['test_docpool_ContentAdministrators']

        # DPDocument is allowed
        self.assertEqual(
            [i.id for i in folder.allowedContentTypes()],
            [
                'Collection',
                'InfoFolder',
                'DPDocument',
                'SimpleFolder',
                'ReviewFolder',
                'CollaborationFolder',
                'PrivateFolder',
                'SRFolder',
            ],
        )

        # but not for the current user...
        from docpool.base.utils import getAllowedDocumentTypes

        self.assertFalse(bool(getAllowedDocumentTypes(folder)))

        # add a user to test with
        user = api.user.create(
            email=u'foo@plone.org', username=u'foo', password=u'secret'
        )

        # add the user to the groups
        api.group.add_user(groupname='test_docpool_ContentAdministrators', user=user)
        docpool_contentadmins = api.group.get('test_docpool_ContentAdministrators')
        # enable all doctypes for this group
        docpool_contentadmins.setGroupProperties({'allowedDocTypes': doctypes_ids})

        # login as a the new user
        logout()
        login(self.portal, 'foo')

        # now this user can add dpdocument using all doctypes
        self.assertEqual(
            set([i.id for i in getAllowedDocumentTypes(folder)]), set(doctypes_ids)
        )
        from docpool.base.utils import getAllowedDocumentTypesForGroup

        self.assertEqual(
            set([i.id for i in getAllowedDocumentTypesForGroup(folder)]),
            set(doctypes_ids),
        )

        # portal_types are still the same
        self.assertEqual(
            [i.id for i in folder.allowedContentTypes()],
            [
                'Collection',
                'InfoFolder',
                'DPDocument',
                'SimpleFolder',
                'ReviewFolder',
                'CollaborationFolder',
                'PrivateFolder',
                'SRFolder',
            ],
        )

        # add a dpdocument of type weatherinformation
        weatherinfo = api.content.create(
            container=folder,
            type='DPDocument',
            title=u'Some Document',
            description=u'foo',
            docType='weatherinformation',
        )
        self.assertEqual(
            weatherinfo.created_by, u'foo <i>Content Administrators (Test Dokpool)</i>'
        )

        eventinfo = api.content.create(
            container=folder,
            type='DPDocument',
            title=u'Some Document',
            description=u'foo',
            docType='eventinformation',
        )
        modified(weatherinfo)
        modified(eventinfo)

        # they can be found using the index dp_type
        self.assertEqual(
            len(
                api.content.find(portal_type='DPDocument', dp_type='weatherinformation')
            ),
            1,
        )
        self.assertEqual(
            len(api.content.find(portal_type='DPDocument', dp_type='eventinformation')),
            1,
        )

        # only the one is reindexed
        self.assertEqual(len(api.content.find(Description=u'foo')), 2)
        self.assertEqual(len(api.content.find(Description=u'bar')), 0)
        weatherinfo.description = u'bar'
        eventinfo.description = u'bar'

        # they are not reindexed when changed like this
        self.assertEqual(len(api.content.find(Description=u'bar')), 0)

        # get the base-doctype for one of the two
        weatherinfo_template = docpool['config']['dtypes']['weatherinformation']

        # trigger reindexing content derived from this
        notify(EditFinishedEvent(weatherinfo_template))

        # only that one was reindexed
        self.assertEqual(len(api.content.find(Description=u'foo')), 1)
        self.assertEqual(len(api.content.find(Description=u'bar')), 1)