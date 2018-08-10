# -*- coding: utf-8 -*-
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from docpool.config.utils import ID, TYPE, TITLE, CHILDREN, createPloneObjects, _addAllowedTypes
from Products.CMFCore.utils import getToolByName
from zope.component.hooks import getSite
from plone import api

import transaction


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Hide uninstall profile from site-creation and quickinstaller."""
        return [
            'docpool.doksys:uninstall',
        ]


def post_install(context):
    """Post install script"""
    # Do something at the end of the installation of this package.
    fresh = True
    createStructure(getSite(), fresh)


def uninstall(context):
    """Uninstall script"""
    # Do something at the end of the uninstallation of this package.



def createStructure(plonesite, fresh):
    changedoksysNavigation(plonesite, fresh)
    transaction.commit()
    create_1day_collection(plonesite)
    transaction.commit()
    create_purpose_collections(plonesite)
    transaction.commit()
    create_sample_collections(plonesite)
    transaction.commit()
    changedoksysDocTypes(plonesite, fresh)
    transaction.commit()

def changedoksysNavigation(plonesite, fresh):
    createPloneObjects(plonesite, BASICSTRUCTURE, fresh)


def changedoksysDocTypes (plonesite, fresh):
    createPloneObjects(plonesite.config.dtypes, DTYPES, fresh)

def create_1day_collection(plonesite):
    api.content.create(
        type='Collection',
        title='Dokumente der letzten 24 h',
        query=[{
            u'i': u'portal_type',
            u'o': u'plone.app.querystring.operation.selection.is',
            u'v': u'DPDocument'
        },
        {
            u'i': u'modified',
            u'o': u'plone.app.querystring.operation.date.beforeToday',
            u'v': u'1d'
        }],
        sort_on='changed',
        sort_order='reverse',
        container=api.content.get(path='/search')
    )
    print "1day Collection angelegt"

def create_purpose_collections(plonesite):
    api.content.create(
        type='Collection',
        title='Standard-Info Bundesmessnetze',
        query=[{
            u'i': u'portal_type',
            u'o': u'plone.app.querystring.operation.selection.is',
            u'v': u'DPDocument'
        },
        {
            u'i': u'purpose',
            u'o': u'plone.app.querystring.operation.string.is',
            u'v': u'Standard-Info Bundesmessnetze'
        }],
        sort_on='changed',
        sort_order='reverse',
        container=api.content.get(path='/search')
    )
    #
    api.content.create(
        type='Collection',
        title='Standard-Info DWD',
        query=[{
            u'i': u'portal_type',
            u'o': u'plone.app.querystring.operation.selection.is',
            u'v': u'DPDocument'
        },
            {
                u'i': u'purpose',
                u'o': u'plone.app.querystring.operation.string.is',
                u'v': u'Standard-Info DWD'
            }],
        sort_on='changed',
        sort_order='reverse',
        container=api.content.get(path='/search')
    )
    print "Purpose Collection angelegt"


def create_sample_collections(plonesite):
    api.content.create(
        type='Collection',
        title='Ergebnisse Boden',
        query=[{
            u'i': u'portal_type',
            u'o': u'plone.app.querystring.operation.selection.is',
            u'v': u'DPDocument'
        },
        {
            u'i': u'sample_type_id',
            u'o': u'plone.app.querystring.operation.string.contains',
            u'v': u'B'
        }],
        sort_on='changed',
        sort_order='reverse',
        container=api.content.get(path='/search')
    )
    api.content.create(
        type='Collection',
        title='Ergebnisse Futtermittel',
        query=[{
            u'i': u'portal_type',
            u'o': u'plone.app.querystring.operation.selection.is',
            u'v': u'DPDocument'
        },
            {
                u'i': u'sample_type_id',
                u'o': u'plone.app.querystring.operation.string.contains',
                u'v': u'F'
            }],
        sort_on='changed',
        sort_order='reverse',
        container=api.content.get(path='/search')
    )
    api.content.create(
        type='Collection',
        title='Ergebnisse Gewaesser',
        query=[{
            u'i': u'portal_type',
            u'o': u'plone.app.querystring.operation.selection.is',
            u'v': u'DPDocument'
        },
            {
                u'i': u'sample_type_id',
                u'o': u'plone.app.querystring.operation.string.contains',
                u'v': u'G'
            }],
        sort_on='changed',
        sort_order='reverse',
        container=api.content.get(path='/search')
    )
    api.content.create(
        type='Collection',
        title='Ergebnisse Luft',
        query=[{
            u'i': u'portal_type',
            u'o': u'plone.app.querystring.operation.selection.is',
            u'v': u'DPDocument'
        },
            {
                u'i': u'sample_type_id',
                u'o': u'plone.app.querystring.operation.string.contains',
                u'v': u'L'
            }],
        sort_on='changed',
        sort_order='reverse',
        container=api.content.get(path='/search')
    )
    api.content.create(
        type='Collection',
        title='Ergebnisse Nahrungsmittel',
        query=[{
            u'i': u'portal_type',
            u'o': u'plone.app.querystring.operation.selection.is',
            u'v': u'DPDocument'
        },
            {
                u'i': u'sample_type_id',
                u'o': u'plone.app.querystring.operation.string.contains',
                u'v': u'N'
            }],
        sort_on='changed',
        sort_order='reverse',
        container=api.content.get(path='/search')
    )
    api.content.create(
        type='Collection',
        title='Ergebnisse Stoerfall',
        query=[{
            u'i': u'portal_type',
            u'o': u'plone.app.querystring.operation.selection.is',
            u'v': u'DPDocument'
        },
            {
                u'i': u'sample_type_id',
                u'o': u'plone.app.querystring.operation.string.contains',
                u'v': u'S'
            }],
        sort_on='changed',
        sort_order='reverse',
        container=api.content.get(path='/search')
    )
    print "Sample Type Collection angelegt"



BASICSTRUCTURE = [
    {
        TYPE: 'Folder',
        TITLE: 'Predefined Searches',
        ID: 'search',
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

DTYPES = [{TYPE: 'DocType', TITLE: u'Dokument', ID: 'dok',
          CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
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
