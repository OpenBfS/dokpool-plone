# -*- coding: utf-8 -*-
from __future__ import print_function
from docpool.config.utils import CHILDREN
from docpool.config.utils import createPloneObjects
from docpool.config.utils import ID
from docpool.config.utils import TITLE
from docpool.config.utils import TYPE
from persistent.list import PersistentList
from plone import api
from plone.app.textfield.value import RichTextValue
from Products.CMFPlone.interfaces import INonInstallable
from Products.CMFPlone.utils import _createObjectByType
from zope.component.hooks import getSite
from zope.interface import implementer

import transaction
import logging

log = logging.getLogger(__name__)


@implementer(INonInstallable)
class HiddenProfiles(object):
    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return ['docpool.doksys:uninstall']


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    fresh = True
    createStructure(context, getSite(), fresh)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.


def createStructure(context, plonesite, fresh):
    changedoksysNavigation(plonesite, fresh)
    s = context.restrictedTraverse('searches')
    s.manage_addProperty('text', '', 'string')
    transaction.commit()
    create_today_collection(plonesite)
    transaction.commit()
    create_since_yesterday_collection(plonesite)
    transaction.commit()
    create_purpose_collections(plonesite)
    transaction.commit()
    create_sample_collections(plonesite)
    transaction.commit()
    changedoksysDocTypes(plonesite, fresh)
    transaction.commit()


def changedoksysNavigation(plonesite, fresh):
    createPloneObjects(plonesite, BASICSTRUCTURE, fresh)


def changedoksysDocTypes(plonesite, fresh):
    createPloneObjects(plonesite.config.dtypes, DTYPES, fresh)


def create_today_collection(plonesite):
    container = api.content.get(path='/searches')
    title = u'Dokumente von Heute'
    description = u'Dokumente seit heute 0:00 Uhr'
    _createObjectByType(
        'Collection', container, id='today', title=title, description=description
    )
    today = container['today']

    # Set the Collection criteria.
    #: Sort on the Effective date
    today.sort_on = u'changed'
    today.sort_reversed = True
    today.relatedItems = ""
    #: Query by Type and Review State
    today.query = [
        {
            'i': u'portal_type',
            'o': u'plone.app.querystring.operation.selection.any',
            'v': [u'DPDocument'],
        },
        {
            u'i': u'created',
            u'o': u'plone.app.querystring.operation.date.today',
            u'v': u'',
        },
        {
            u'i': u'OperationMode',
            u'o': u'plone.app.querystring.operation.selection.any',
            u'v': [u'Intensiv', u'Routine'],
        },
    ]
    today.text = RichTextValue('', 'text/html', 'text/x-html-safe')
    today.setLayout('docpool_collection_view')
    log.info('Collection "Dokumente von Heute" angelegt')
    return today


def create_since_yesterday_collection(plonesite):
    container = api.content.get(path='/searches')
    title = u'Dokumente seit Gestern'
    description = u'Dokumente der letzten 24 Stunden'
    _createObjectByType(
        'Collection', container, id='yesterday', title=title, description=description
    )
    yesterday = container['yesterday']

    # Set the Collection criteria.
    #: Sort on the Effective date
    yesterday.sort_on = u'changed'
    yesterday.sort_reversed = True
    yesterday.relatedItems = ""
    #: Query by Type and Review State
    yesterday.query = [
        {
            'i': u'portal_type',
            'o': u'plone.app.querystring.operation.selection.any',
            'v': [u'DPDocument'],
        },
        {
            u'i': u'creationDate',
            u'o': u'plone.app.querystring.operation.date.largerThanRelativeDate',
            u'v': u'-1',
        },
        {
            u'i': u'OperationMode',
            u'o': u'plone.app.querystring.operation.selection.any',
            u'v': [u'Intensiv', u'Routine'],
        },
    ]
    yesterday.text = RichTextValue('', 'text/html', 'text/x-html-safe')
    yesterday.setLayout('docpool_collection_view')
    log.info('Collection "Dokumente seit Gestern" angelegt')
    return yesterday

def create_purpose_collections(plonesite):
    container = api.content.get(path='/searches')
    title = 'Standard-Info Bundesmessnetze'
    description = 'Standard-Info Bundesmessnetze'
    _createObjectByType(
        'Collection',
        container,
        id='bundesmessnetze',
        title=title,
        description=description,
    )
    iwas = container['bundesmessnetze']

    # Set the Collection criteria.
    #: Sort on the Effective date
    iwas.sort_on = u'effective'
    iwas.sort_reversed = True
    iwas.relatedItems = ""
    #: Query by Type and Review State
    iwas.query = [
        {
            'i': u'portal_type',
            'o': u'plone.app.querystring.operation.selection.any',
            'v': [u'DPDocument'],
        },
        {
            u'i': u'Purpose',
            u'o': u'plone.app.querystring.operation.string.is',
            u'v': u'Standard-Info Bundesmessnetze',
        },
    ]
    iwas.text = RichTextValue(
        '<p>Standard-Info Bundesmessnetze<p>', 'text/html', 'text/x-html-safe'
    )
    iwas.setLayout('docpool_collection_view')

    title = 'Standard-Info DWD'
    description = 'Standard-Info DWD'
    _createObjectByType(
        'Collection', container, id='dwd', title=title, description=description
    )
    iwas = container['dwd']

    # Set the Collection criteria.
    #: Sort on the Effective date
    iwas.sort_on = u'effective'
    iwas.sort_reversed = True
    iwas.relatedItems = ""
    #: Query by Type and Review State
    iwas.query = [
        {
            'i': u'portal_type',
            'o': u'plone.app.querystring.operation.selection.any',
            'v': [u'DPDocument'],
        },
        {
            u'i': u'Purpose',
            u'o': u'plone.app.querystring.operation.string.is',
            u'v': u'Standard-Info Bundesmessnetze',
        },
    ]
    iwas.text = RichTextValue(
        '<p>Standard-Info DWD<p>', 'text/html', 'text/x-html-safe'
    )
    iwas.setLayout('docpool_collection_view')
    #

    print("Purpose Collection angelegt")


def create_sample_collections(plonesite):
    container = api.content.get(path='/searches')
    title = 'Ergebnisse Boden'
    description = 'Ergebnisse Boden'
    _createObjectByType(
        'Collection', container, id='boden', title=title, description=description
    )
    iwas = container['boden']

    # Set the Collection criteria.
    #: Sort on the Effective date
    iwas.sort_on = u'effective'
    iwas.sort_reversed = True
    iwas.relatedItems = ""
    #: Query by Type and Review State
    iwas.query = [
        {
            'i': u'portal_type',
            'o': u'plone.app.querystring.operation.selection.any',
            'v': [u'DPDocument'],
        },
        {
            u'i': u'SampleTypeId',
            u'o': u'plone.app.querystring.operation.string.contains',
            u'v': u'B*',
        },
    ]
    iwas.text = RichTextValue(
        '<p>Ergebnisse Boden<p>',
        'text/html',
        'text/x-html-safe')
    iwas.setLayout('docpool_collection_view')

    title = 'Ergebnisse Futtermittel'
    description = 'Ergebnisse Futtermittel'
    _createObjectByType(
        'Collection', container, id='futter', title=title, description=description
    )
    iwas = container['futter']

    # Set the Collection criteria.
    #: Sort on the Effective date
    iwas.sort_on = u'effective'
    iwas.sort_reversed = True
    iwas.relatedItems = ""
    #: Query by Type and Review State
    iwas.query = [
        {
            'i': u'portal_type',
            'o': u'plone.app.querystring.operation.selection.any',
            'v': [u'DPDocument'],
        },
        {
            u'i': u'SampleTypeId',
            u'o': u'plone.app.querystring.operation.string.contains',
            u'v': u'F*',
        },
    ]
    iwas.text = RichTextValue(
        '<p>Ergebnisse Futtermittel<p>', 'text/html', 'text/x-html-safe'
    )
    iwas.setLayout('docpool_collection_view')

    title = 'Ergebnisse Gewaesser'
    description = 'Ergebnisse Gewaesser'
    _createObjectByType(
        'Collection', container, id='wasser', title=title, description=description
    )
    iwas = container['wasser']

    # Set the Collection criteria.
    #: Sort on the Effective date
    iwas.sort_on = u'effective'
    iwas.sort_reversed = True
    iwas.relatedItems = ""
    #: Query by Type and Review State
    iwas.query = [
        {
            'i': u'portal_type',
            'o': u'plone.app.querystring.operation.selection.any',
            'v': [u'DPDocument'],
        },
        {
            u'i': u'SampleTypeId',
            u'o': u'plone.app.querystring.operation.string.contains',
            u'v': u'G*',
        },
    ]
    iwas.text = RichTextValue(
        '<p>Ergebnisse Gewaesser<p>', 'text/html', 'text/x-html-safe'
    )
    iwas.setLayout('docpool_collection_view')

    title = 'Ergebnisse Luft'
    description = 'Ergebnisse Luft'
    _createObjectByType(
        'Collection', container, id='luft', title=title, description=description
    )
    iwas = container['luft']

    # Set the Collection criteria.
    #: Sort on the Effective date
    iwas.sort_on = u'effective'
    iwas.sort_reversed = True
    iwas.relatedItems = ""
    #: Query by Type and Review State
    iwas.query = [
        {
            'i': u'portal_type',
            'o': u'plone.app.querystring.operation.selection.any',
            'v': [u'DPDocument'],
        },
        {
            u'i': u'SampleTypeId',
            u'o': u'plone.app.querystring.operation.string.contains',
            u'v': u'L*',
        },
    ]
    iwas.text = RichTextValue(
        '<p>Ergebnisse Luft<p>',
        'text/html',
        'text/x-html-safe')
    iwas.setLayout('docpool_collection_view')

    title = 'Ergebnisse Nahrungsmittel'
    description = 'Ergebnisse Nahrungsmittel'
    _createObjectByType(
        'Collection', container, id='nahrung', title=title, description=description
    )
    iwas = container['nahrung']

    # Set the Collection criteria.
    #: Sort on the Effective date
    iwas.sort_on = u'effective'
    iwas.sort_reversed = True
    iwas.relatedItems = ""
    #: Query by Type and Review State
    iwas.query = [
        {
            'i': u'portal_type',
            'o': u'plone.app.querystring.operation.selection.any',
            'v': [u'DPDocument'],
        },
        {
            u'i': u'SampleTypeId',
            u'o': u'plone.app.querystring.operation.string.contains',
            u'v': u'N*',
        },
    ]
    iwas.text = RichTextValue(
        '<p>Ergebnisse Nahrungsmittel<p>', 'text/html', 'text/x-html-safe'
    )
    iwas.setLayout('docpool_collection_view')

    title = 'Ergebnisse Stoerfall'
    description = 'Ergebnisse Stoerfall'
    _createObjectByType(
        'Collection', container, id='stoer', title=title, description=description
    )
    iwas = container['stoer']

    # Set the Collection criteria.
    #: Sort on the Effective date
    iwas.sort_on = u'effective'
    iwas.sort_reversed = True
    iwas.relatedItems = ""
    #: Query by Type and Review State
    iwas.query = [
        {
            'i': u'portal_type',
            'o': u'plone.app.querystring.operation.selection.any',
            'v': [u'DPDocument'],
        },
        {
            u'i': u'SampleTypeId',
            u'o': u'plone.app.querystring.operation.string.contains',
            u'v': u'S*',
        },
    ]
    iwas.text = RichTextValue(
        '<p>Ergebnisse Stoerfall<p>', 'text/html', 'text/x-html-safe'
    )
    iwas.setLayout('docpool_collection_view')

    print("Sample Type Collection angelegt")


BASICSTRUCTURE = [
    {
        TYPE: 'Folder',
        TITLE: 'Predefined Searches',
        ID: 'searches',
        # TODO: relatedItems broken when creating a doksys docpool.
        # See https://redmine-koala.bfs.de/issues/3291
        # and https://redmine-koala.bfs.de/issues/3350
        # 'relatedItems': PersistentList(),
        CHILDREN: [
            #            {
            #                TYPE: 'Folder',
            #                TITLE: 'Ordner',
            #                ID: 'lastday'
            #            }
        ],  # TODO: further folders filled with Doksys Collections
    }
    # {
    #    TYPE: 'DPInfos', # when type is available
    #     TITLE: 'Infos',
    #     ID: 'doksys-infos',
    #     CHILDREN: [
    #         {
    #             TYPE: 'InfoFolder',
    #             TITLE: 'Infos zu...',
    #             ID: 'info1'
    #         }
    #     ],
    # }
]

# doctypes definitions
# uncomment when when elan.py is removed from dokpool.config.general
# CHANGE HERE. DocTypes, DocCollections and their connections must match.

DTYPES = [
    {
        TYPE: 'DocType',
        TITLE: u'DoksysDokument',
        ID: 'doksysdok',
        CHILDREN: [],
        'local_behaviors': ['doksys'],
    },
    #         {TYPE: 'DocType', TITLE: u'Mitteilung', ID: 'note',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #          {TYPE: 'DocType', TITLE: u'Ereignisinformation', ID: 'eventinformation',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #          {TYPE: 'DocType', TITLE: u'Anlageninformation', ID: 'nppinformation',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #          {TYPE: 'DocType', TITLE: u'Wetterinformation', ID: 'weatherinformation',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #          {TYPE: 'DocType', TITLE: u'Trajektorie', ID: 'trajectory',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #          {TYPE: 'DocType', TITLE: u'RODOS_Prognose', ID: 'rodosprojection',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #          {TYPE: 'DocType', TITLE: u'Prognose_Land', ID: 'stateprojection',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #          {TYPE: 'DocType', TITLE: u'Andere_Prognose', ID: 'otherprojection',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #          {TYPE: 'DocType', TITLE: u'Messergebnis_ODL', ID: 'gammadoserate',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #          {TYPE: 'DocType', TITLE: u'Messergebnis_ODL_Zeitreihe', ID: 'gammadoserate_timeseries',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #          {TYPE: 'DocType', TITLE: u'Messergebnis_ODL_Messspur', ID: 'gammadoserate_mobile',
    #          CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #          {TYPE: 'DocType', TITLE: u'Messergebnis_Luftaktivität', ID: 'airactivity',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #          {TYPE: 'DocType', TITLE: u'Messergebnis_insitu', ID: 'mresult_insitu',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #          {TYPE: 'DocType', TITLE: u'Messergebnis_Bodenkontamination', ID: 'groundcontamination',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #          {TYPE: 'DocType', TITLE: u'Messergebnis_Futtermittel', ID: 'mresult_feed',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #          {TYPE: 'DocType', TITLE: u'Messergebnis_Lebensmittel', ID: 'mresult_food',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #          {TYPE: 'DocType', TITLE: u'Messergebnis_Gewässer', ID: 'mresult_water',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #          {TYPE: 'DocType', TITLE: u'Messergebnis_Sonstige', ID: 'mresult_other',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #          {TYPE: 'DocType', TITLE: u'Messergebnis_Aerogamma', ID: 'mresult_flight',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #          {TYPE: 'DocType', TITLE: u'Lageinformation', ID: 'situationreport',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #          {TYPE: 'DocType', TITLE: u'Lagebericht', ID: 'sitrep',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #          {TYPE: 'DocType', TITLE: u'Bewertung', ID: 'estimation',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #          {TYPE: 'DocType', TITLE: u'Maßnahmeninformation', ID: 'instructions',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #          {TYPE: 'DocType', TITLE: u'Maßnahmenempfehlungen', ID: 'protectiveactions',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #          {TYPE: 'DocType', TITLE: u'Pressemitteilung', ID: 'mediarelease',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
    #          {TYPE: 'DocType', TITLE: u'Insitu_Information', ID: 'insituinformation',
    #           CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
]
