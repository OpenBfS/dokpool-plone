# -*- coding: utf-8 -*-
from docpool.config.utils import CHILDREN
from docpool.config.utils import createPloneObjects
from docpool.config.utils import ID
from docpool.config.utils import TITLE
from docpool.config.utils import TYPE
from persistent.list import PersistentList
from plone import api
from Products.CMFCore.utils import getToolByName

import transaction


def install(plonesite):
    """
    """
    fresh = True
    if plonesite.hasObject("doksys"):
        fresh = False  # It's a reinstall
    configUsers(plonesite, fresh)
    createStructure(plonesite, fresh)


def configUsers(plonesite, fresh):
    """
    """
    if fresh:
        mtool = getToolByName(plonesite, "portal_membership")
        mtool.addMember(
            'doksysadmin',
            'Doksys Administrator (global)',
            ['Site Administrator', 'Member'],
            [],
        )
        doksysadmin = mtool.getMemberById('doksysadmin')
        doksysadmin.setMemberProperties({"fullname": 'DokSys Administrator'})
        doksysadmin.setSecurityProfile(password="admin")
        mtool.addMember(
            'doksysmanager', 'DokSys Manager (global)', [
                'Manager', 'Member'], []
        )
        doksysmanager = mtool.getMemberById('doksysmanager')
        doksysmanager.setMemberProperties({"fullname": 'DokSys Manager'})
        doksysmanager.setSecurityProfile(password="admin")
        # Role from rolemap.xml
        api.user.grant_roles(username='doksysmanager', roles=['DoksysUser'])
        api.user.grant_roles(username='doksysadmin', roles=['DoksysUser'])
        api.user.grant_roles(username='dpmanager', roles=['DoksysUser'])
        api.user.grant_roles(username='dpadmin', roles=['DoksysUser'])


def createStructure(plonesite, fresh):
    createDoksysNavigation(plonesite, fresh)
    transaction.commit()
    createDoksysDocTypes(plonesite, fresh)
    transaction.commit()


def createDoksysNavigation(plonesite, fresh):
    createPloneObjects(plonesite, BASICSTRUCTURE, fresh)


def createDoksysDocTypes(plonesite, fresh):
    createPloneObjects(plonesite.config.dtypes, DTYPES, fresh)


BASICSTRUCTURE = [
    {
        TYPE: 'Folder',
        TITLE: 'Predefined Searches',
        ID: 'searches',
        'relatedItems': PersistentList(),
        CHILDREN: [
            {TYPE: 'Folder', TITLE: 'Documents of last 24h', ID: 'lastday'}
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
        TITLE: u'dok',
        ID: 'dok',
        #          CHILDREN: [], 'local_behaviors': ['elan', 'doksys']},
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
        #          {TYPE: 'DocType', TITLE: u'DWD_Prognose', ID: 'weatherserviceprojection',
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
    }
]
