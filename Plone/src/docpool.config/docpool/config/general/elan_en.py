# -*- coding: utf-8 -*-
from docpool.base.events import IDocumentPoolUndeleteable
from docpool.config.utils import CHILDREN
from docpool.config.utils import createPloneObjects
from docpool.config.utils import ID
from docpool.config.utils import TITLE
from docpool.config.utils import TYPE
from docpool.elan.config import ELAN_APP
from plone import api
from plone.app.textfield.value import RichTextValue
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import log_exc
from Products.Five.utilities.marker import mark

import transaction


def install(self):
    """
    """
    fresh = True
    if self.hasObject("esd"):
        fresh = False  # It's a reinstall
    configUsers(self, fresh)
    createStructure(self, fresh)
    if fresh:
        connectTypesAndCategories(self)
    setFrontpage(self)


def configUsers(self, fresh):
    """
    """
    if fresh:
        mtool = getToolByName(self, "portal_membership")
        mtool.addMember(
            'elanadmin',
            'ELAN Administrator (global)',
            ['Site Administrator', 'Member'],
            [],
        )
        elanadmin = mtool.getMemberById('elanadmin')
        elanadmin.setMemberProperties({"fullname": 'ELAN Administrator'})
        elanadmin.setSecurityProfile(password="admin")
        mtool.addMember(
            'elanmanager', 'ELAN Manager (global)', ['Manager', 'Member'], []
        )
        elanmanager = mtool.getMemberById('elanmanager')
        elanmanager.setMemberProperties({"fullname": 'ELAN Manager'})
        elanmanager.setSecurityProfile(password="admin")
        api.user.grant_roles(username='elanmanager', roles=['ELANUser'])
        api.user.grant_roles(username='elanadmin', roles=['ELANUser'])
        api.user.grant_roles(username='dpmanager', roles=['ELANUser'])
        api.user.grant_roles(username='dpadmin', roles=['ELANUser'])


def createStructure(self, fresh):
    createBasicPortalStructure(self, fresh)
    transaction.commit()
    createDocTypes(self, fresh)
    transaction.commit()
    fillBasicPortalStructure(self, fresh)
    transaction.commit()


def createDocTypes(plonesite, fresh):
    """
    """
    createPloneObjects(plonesite.config.dtypes, DTYPES, fresh)


def createBasicPortalStructure(plonesite, fresh):
    """
    """
    createPloneObjects(plonesite, BASICSTRUCTURE, fresh)


def fillBasicPortalStructure(plonesite, fresh):
    """
    """
    createPloneObjects(plonesite, BASICSTRUCTURE2, fresh)
    # Now mark certain objects as undeleteable
    mark(plonesite.esd['front-page'], IDocumentPoolUndeleteable)
    mark(plonesite.esd.overview, IDocumentPoolUndeleteable)
    mark(plonesite.esd.recent, IDocumentPoolUndeleteable)


def setFrontpage(self):
    """
    """
    self.esd.setDefaultPage("front-page")


FRONTPAGE = RichTextValue(u"", 'text/plain', 'text/html')

BASICSTRUCTURE = [
    {
        TYPE: 'ELANCurrentSituation',
        TITLE: 'Current Situation Template',
        ID: 'esd',
        CHILDREN: [
            {
                TYPE: 'Document',
                TITLE: u'Electronic Situation Display',
                ID: 'front-page',
                'text': FRONTPAGE,
                CHILDREN: [],
            }
        ],
    },
    {
        TYPE: 'ELANContentConfig',
        TITLE: 'Content Configuration',
        ID: 'contentconfig',
        CHILDREN: [
            {TYPE: 'Text', TITLE: u'Impressum', ID: 'impressum', CHILDREN: []},
        ],
    },
]
DOCTYPES = (
    'ref_setDocTypesUpdateCollection'
)  # indicates that docTypes is referencing objects, which need to be queried by their id

ESDCOLLECTIONS = [
    {
        TYPE: 'ELANSection',
        TITLE: u'INCIDENT',
        ID: 'incident',
        CHILDREN: [
            {
                TYPE: 'ELANDocCollection',
                TITLE: u'NOTIFICATIONS',
                ID: 'notifications',
                CHILDREN: [],
                DOCTYPES: ['notification', 'note'],
            },
            {
                TYPE: 'ELANDocCollection',
                TITLE: u'EVENT / NPP INFORMATION',
                ID: 'event-npp-information',
                CHILDREN: [],
                DOCTYPES: ['eventinformation', 'nppinformation'],
            },
        ],
    },
    {
        TYPE: 'ELANSection',
        TITLE: u'METEOROLOGY',
        ID: 'meteorology',
        CHILDREN: [
            {
                TYPE: 'ELANDocCollection',
                TITLE: u'WEATHER INFORMATION',
                ID: 'weather-information',
                CHILDREN: [],
                DOCTYPES: ['weatherinformation'],
            },
            {
                TYPE: 'ELANDocCollection',
                TITLE: u'TRAJECTORIES',
                ID: 'trajectories',
                CHILDREN: [],
                DOCTYPES: ['trajectory'],
            },
        ],
    },
    {
        TYPE: 'ELANSection',
        TITLE: u'DOSE PROJECTIONS',
        ID: 'dose-projections',
        CHILDREN: [
            {
                TYPE: 'ELANDocCollection',
                TITLE: u'NPP PROJECTIONS',
                ID: 'npp-projections',
                CHILDREN: [],
                DOCTYPES: ['nppprojection'],
            },
            {
                TYPE: 'ELANDocCollection',
                TITLE: u'RODOS',
                ID: 'rodos',
                CHILDREN: [],
                DOCTYPES: ['rodosprojection'],
            },
            {
                TYPE: 'ELANDocCollection',
                TITLE: u'OTHER',
                ID: 'other',
                CHILDREN: [],
                DOCTYPES: ['otherprojection'],
            },
        ],
    },
    {
        TYPE: 'ELANSection',
        TITLE: u'MEASUREMENT RESULTS',
        ID: 'measurement-results',
        CHILDREN: [
            {
                TYPE: 'ELANDocCollection',
                TITLE: u'GAMMA DOSE RATE',
                ID: 'gamma-dose-rate',
                CHILDREN: [],
                DOCTYPES: ['gammadoserate'],
            },
            {
                TYPE: 'ELANDocCollection',
                TITLE: u'AIR ACTIVITY',
                ID: 'air-activity',
                CHILDREN: [],
                DOCTYPES: ['airactivity'],
            },
            {
                TYPE: 'ELANDocCollection',
                TITLE: u'GROUND CONTAMINATION',
                ID: 'ground-contamination',
                CHILDREN: [],
                DOCTYPES: ['groundcontamination'],
            },
            {
                TYPE: 'ELANDocCollection',
                TITLE: u'FOOD AND FEED',
                ID: 'food-and-feed',
                CHILDREN: [],
                DOCTYPES: ['mresult_feed', 'mresult_food'],
            },
            {
                TYPE: 'ELANDocCollection',
                TITLE: u'WATER',
                ID: 'water',
                CHILDREN: [],
                DOCTYPES: ['mresult_water'],
            },
        ],
    },
    {
        TYPE: 'ELANSection',
        TITLE: u'CURRENT SITUATION',
        ID: 'current-situation',
        CHILDREN: [
            {
                TYPE: 'ELANDocCollection',
                TITLE: u'SITUATION REPORTS',
                ID: 'situation-reports',
                CHILDREN: [],
                DOCTYPES: ['situationreport', 'sitrep'],
            },
            {
                TYPE: 'ELANDocCollection',
                TITLE: u'PROTECTIVE ACTIONS',
                ID: 'protective-actions',
                CHILDREN: [],
                DOCTYPES: ['instructions', 'protectiveactions'],
            },
        ],
    },
    {
        TYPE: 'ELANSection',
        TITLE: u'INFORMATION OF THE PUBLIC',
        ID: 'information-of-the-public',
        CHILDREN: [
            {
                TYPE: 'ELANDocCollection',
                TITLE: u'MEDIA RELEASES',
                ID: 'media-releases',
                CHILDREN: [],
                DOCTYPES: ['mediarelease'],
            },
            {
                TYPE: 'ELANDocCollection',
                TITLE: u'INSTRUCTIONS TO THE PUBLIC',
                ID: 'instructions-to-the-public',
                CHILDREN: [],
                DOCTYPES: ['instructions'],
            },
        ],
    },
    {
        TYPE: 'ELANDocCollection',
        TITLE: 'Overview',
        ID: 'overview',
        "setExcludeFromNav": True,
        DOCTYPES: [],
        CHILDREN: [],
    },
    {
        TYPE: 'ELANDocCollection',
        TITLE: 'All documents',
        ID: 'recent',
        "setExcludeFromNav": True,
        DOCTYPES: [],
        CHILDREN: [],
    },
    {TYPE: 'Dashboard', TITLE: 'Dashboard',
        ID: 'dashboard', "setExcludeFromNav": True},
    {
        TYPE: 'SituationOverview',
        TITLE: 'Situation overview',
        ID: 'situationoverview',
        "setExcludeFromNav": True,
    },
]

BASICSTRUCTURE2 = [
    {
        TYPE: 'ELANCurrentSituation',
        TITLE: 'Current Situation Template',
        ID: 'esd',
        CHILDREN: ESDCOLLECTIONS,
    }
]

# Structure definitions
# CHANGE HERE. DocTypes, DocCollections and their connections must match.

DTYPES = [
    {
        TYPE: 'DocType',
        TITLE: u'Notification',
        ID: 'notification',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Note',
        ID: 'note',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Event Information',
        ID: 'eventinformation',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'NPP Information',
        ID: 'nppinformation',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Weather Information',
        ID: 'weatherinformation',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Trajectory',
        ID: 'trajectory',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'NPP Projection',
        ID: 'nppprojection',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'RODOS Projection',
        ID: 'rodosprojection',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Other Projection',
        ID: 'otherprojection',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Gamma Dose Rate',
        ID: 'gammadoserate',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Air Activity',
        ID: 'airactivity',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Ground Contamination',
        ID: 'groundcontamination',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Measurement Result Feed',
        ID: 'mresult_feed',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Measurement Result Food',
        ID: 'mresult_food',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Measurement Result Water',
        ID: 'mresult_water',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Situation Description',
        ID: 'situationreport',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Situation Report',
        ID: 'sitrep',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Instructions to the Public',
        ID: 'instructions',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Protective Actions',
        ID: 'protectiveactions',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Media Release',
        ID: 'mediarelease',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
]

def connectTypesAndCategories(self):
    """
    """

    # print self.config.dtypes.eventinformation.type_extension(ELAN_APP)
    try:
        self.config.dtypes.notification.type_extension(ELAN_APP).setCCategory(
            'notifications'
        )
    except Exception as e:
        log_exc(e)
    try:
        self.config.dtypes.note.type_extension(
            ELAN_APP).setCCategory('notifications')
    except BaseException:
        pass
    try:
        self.config.dtypes.eventinformation.type_extension(ELAN_APP).setCCategory(
            'event-npp-information'
        )
    except BaseException:
        pass
    try:
        self.config.dtypes.nppinformation.type_extension(ELAN_APP).setCCategory(
            'event-npp-information'
        )
    except BaseException:
        pass
    try:
        self.config.dtypes.weatherinformation.type_extension(ELAN_APP).setCCategory(
            'weather-information'
        )
    except BaseException:
        pass
    try:
        self.config.dtypes.trajectory.type_extension(ELAN_APP).setCCategory(
            'trajectories'
        )
    except BaseException:
        pass
    try:
        self.config.dtypes.rodosprojection.type_extension(ELAN_APP).setCCategory(
            'rodos-projections'
        )
    except BaseException:
        pass
    try:
        self.config.dtypes.stateprojection.type_extension(ELAN_APP).setCCategory(
            'state-projections'
        )
    except BaseException:
        pass
    try:
        self.config.dtypes.otherprojection.type_extension(ELAN_APP).setCCategory(
            'other-projections'
        )
    except BaseException:
        pass
    try:
        self.config.dtypes.gammadoserate.type_extension(ELAN_APP).setCCategory(
            'gamma-dose-rate'
        )
    except BaseException:
        pass
    try:
        self.config.dtypes.gammadoserate_timeseries.type_extension(ELAN_APP).setCCategory(
            'gamma-dose-rate'
        )
    except BaseException:
        pass
    try:
        self.config.dtypes.gammadoserate_mobile.type_extension(ELAN_APP).setCCategory(
            'gamma-dose-rate'
        )
    except BaseException:
        pass
    try:
        self.config.dtypes.airactivity.type_extension(ELAN_APP).setCCategory(
            'air-activity'
        )
    except BaseException:
        pass
    try:
        self.config.dtypes.groundcontamination.type_extension(ELAN_APP).setCCategory(
            'ground-contamination'
        )
    except BaseException:
        pass
    try:
        self.config.dtypes.mresult_feed.type_extension(ELAN_APP).setCCategory(
            'food-and-feed'
        )
    except BaseException:
        pass
    try:
        self.config.dtypes.mresult_food.type_extension(ELAN_APP).setCCategory(
            'food-and-feed'
        )
    except BaseException:
        pass
    try:
        self.config.dtypes.mresult_water.type_extension(
            ELAN_APP).setCCategory('water')
    except BaseException:
        pass
    try:
        self.config.dtypes.situationreport.type_extension(ELAN_APP).setCCategory(
            'situation-reports'
        )
    except BaseException:
        pass
    try:
        self.config.dtypes.sitrep.type_extension(ELAN_APP).setCCategory(
            'situation-reports'
        )
    except BaseException:
        pass
    try:
        self.config.dtypes.estimation.type_extension(ELAN_APP).setCCategory(
            'protective-actions'
        )
    except BaseException:
        pass
    try:
        self.config.dtypes.instructions.type_extension(ELAN_APP).setCCategory(
            'protective-actions'
        )
    except BaseException:
        pass
    try:
        self.config.dtypes.protectiveactions.type_extension(ELAN_APP).setCCategory(
            'protective-actions'
        )
    except BaseException:
        pass
    try:
        self.config.dtypes.mediarelease.type_extension(ELAN_APP).setCCategory(
            'media-releases'
        )
    except BaseException:
        pass
    try:
        self.config.dtypes.instructions.type_extension(ELAN_APP).setCCategory(
            'instructions-to-the-public'
        )
    except BaseException:
        pass
