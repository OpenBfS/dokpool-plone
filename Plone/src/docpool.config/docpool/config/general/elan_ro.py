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


FRONTPAGE = RichTextValue("", 'text/plain', 'text/html')

BASICSTRUCTURE = [
    {
        TYPE: 'ELANCurrentSituation',
        TITLE: 'Current Situation Template',
        ID: 'esd',
        CHILDREN: [
            {
                TYPE: 'Document',
                TITLE: 'Electronic Situation Display',
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
            {TYPE: 'Text', TITLE: 'Impressum', ID: 'impressum', CHILDREN: []},
        ],
    },
]
DOCTYPES = (
    'ref_setDocTypesUpdateCollection'
)  # indicates that docTypes is referencing objects, which need to be queried by their id

ESDCOLLECTIONS = [
    {
        TYPE: 'ELANSection',
        TITLE: 'INCIDENT',
        ID: 'incident',
        CHILDREN: [
            {
                TYPE: 'ELANDocCollection',
                TITLE: 'NOTIFICATIONS',
                ID: 'notifications',
                CHILDREN: [],
                DOCTYPES: ['notification', 'note'],
            },
            {
                TYPE: 'ELANDocCollection',
                TITLE: 'EVENT / NPP INFORMATION',
                ID: 'event-npp-information',
                CHILDREN: [],
                DOCTYPES: ['eventinformation', 'nppinformation'],
            },
        ],
    },
    {
        TYPE: 'ELANSection',
        TITLE: 'METEOROLOGY',
        ID: 'meteorology',
        CHILDREN: [
            {
                TYPE: 'ELANDocCollection',
                TITLE: 'WEATHER INFORMATION',
                ID: 'weather-information',
                CHILDREN: [],
                DOCTYPES: ['weatherinformation'],
            },
            {
                TYPE: 'ELANDocCollection',
                TITLE: 'TRAJECTORIES',
                ID: 'trajectories',
                CHILDREN: [],
                DOCTYPES: ['trajectory'],
            },
        ],
    },
    {
        TYPE: 'ELANSection',
        TITLE: 'DOSE PROJECTIONS',
        ID: 'dose-projections',
        CHILDREN: [
            {
                TYPE: 'ELANDocCollection',
                TITLE: 'CNCAN PROJECTIONS',
                ID: 'cncan-projections',
                CHILDREN: [],
                DOCTYPES: ['cncanprojection'],
            },
            {
                TYPE: 'ELANDocCollection',
                TITLE: 'IFIN PROJECTIONS',
                ID: 'ifin-projections',
                CHILDREN: [],
                DOCTYPES: ['ifinprojection'],
            },
            {
                TYPE: 'ELANDocCollection',
                TITLE: 'NPP PROJECTIONS',
                ID: 'npp-projections',
                CHILDREN: [],
                DOCTYPES: ['nppprojection'],
            },
            {
                TYPE: 'ELANDocCollection',
                TITLE: 'RODOS',
                ID: 'rodos',
                CHILDREN: [],
                DOCTYPES: ['rodosprojection'],
            },
            {
                TYPE: 'ELANDocCollection',
                TITLE: 'OTHER',
                ID: 'other',
                CHILDREN: [],
                DOCTYPES: ['otherprojection'],
            },
        ],
    },
    {
        TYPE: 'ELANSection',
        TITLE: 'MEASUREMENT RESULTS',
        ID: 'measurement-results',
        CHILDREN: [
            {
                TYPE: 'ELANDocCollection',
                TITLE: 'GAMMA DOSE RATE',
                ID: 'gamma-dose-rate',
                CHILDREN: [],
                DOCTYPES: ['gammadoserate'],
            },
            {
                TYPE: 'ELANDocCollection',
                TITLE: 'AIR ACTIVITY',
                ID: 'air-activity',
                CHILDREN: [],
                DOCTYPES: ['airactivity'],
            },
            {
                TYPE: 'ELANDocCollection',
                TITLE: 'GROUND CONTAMINATION',
                ID: 'ground-contamination',
                CHILDREN: [],
                DOCTYPES: ['groundcontamination'],
            },
            {
                TYPE: 'ELANDocCollection',
                TITLE: 'FOOD AND FEED',
                ID: 'food-and-feed',
                CHILDREN: [],
                DOCTYPES: ['mresult_feed', 'mresult_food'],
            },
            {
                TYPE: 'ELANDocCollection',
                TITLE: 'WATER',
                ID: 'water',
                CHILDREN: [],
                DOCTYPES: ['mresult_water'],
            },
        ],
    },
    {
        TYPE: 'ELANSection',
        TITLE: 'CURRENT SITUATION',
        ID: 'current-situation',
        CHILDREN: [
            {
                TYPE: 'ELANDocCollection',
                TITLE: 'SITUATION REPORTS',
                ID: 'situation-reports',
                CHILDREN: [],
                DOCTYPES: ['nppinformation', 'situationreport', 'sitrep'],
            },
            {
                TYPE: 'ELANDocCollection',
                TITLE: 'PROTECTIVE ACTIONS',
                ID: 'protective-actions',
                CHILDREN: [],
                DOCTYPES: ['instructions', 'protectiveactions'],
            },
        ],
    },
    {
        TYPE: 'ELANSection',
        TITLE: 'INFORMATION OF THE PUBLIC',
        ID: 'information-of-the-public',
        CHILDREN: [
            {
                TYPE: 'ELANDocCollection',
                TITLE: 'MEDIA RELEASES',
                ID: 'media-releases',
                CHILDREN: [],
                DOCTYPES: ['mediarelease'],
            },
            {
                TYPE: 'ELANDocCollection',
                TITLE: 'INSTRUCTIONS TO THE PUBLIC',
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
        TITLE: 'Notification',
        ID: 'notification',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: 'Note',
        ID: 'note',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: 'Event Information',
        ID: 'eventinformation',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: 'NPP Information',
        ID: 'nppinformation',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: 'Weather Information',
        ID: 'weatherinformation',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: 'Trajectory',
        ID: 'trajectory',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: 'CNCAN Projection',
        ID: 'cncanprojection',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: 'IFIN Projection',
        ID: 'ifinprojection',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: 'NPP Projection',
        ID: 'nppprojection',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: 'RODOS Projection',
        ID: 'rodosprojection',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: 'Other Projection',
        ID: 'otherprojection',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: 'Gamma Dose Rate',
        ID: 'gammadoserate',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: 'Air Activity',
        ID: 'airactivity',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: 'Ground Contamination',
        ID: 'groundcontamination',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: 'Measurement Result Feed',
        ID: 'mresult_feed',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: 'Measurement Result Food',
        ID: 'mresult_food',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: 'Measurement Result Water',
        ID: 'mresult_water',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: 'Situation Description',
        ID: 'situationreport',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: 'Situation Report',
        ID: 'sitrep',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: 'Instructions to the Public',
        ID: 'instructions',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: 'Protective Actions',
        ID: 'protectiveactions',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
    {
        TYPE: 'DocType',
        TITLE: 'Media Release',
        ID: 'mediarelease',
        CHILDREN: [],
        'local_behaviors': ['elan'],
    },
]


def connectTypesAndCategories(self):
    """
    """

    #        print self.config.dtypes.eventinformation.type_extension(ELAN_APP)
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
        self.config.dtypes.cncanprojection.type_extension(ELAN_APP).setCCategory(
            'cncan-projections'
        )
    except BaseException:
        pass
    try:
        self.config.dtypes.ifinprojection.type_extension(ELAN_APP).setCCategory(
            'ifin-projections'
        )
    except BaseException:
        pass
    try:
        self.config.dtypes.nppprojection.type_extension(ELAN_APP).setCCategory(
            'npp-projections'
        )
    except BaseException:
        pass
    try:
        self.config.dtypes.rodosprojection.type_extension(ELAN_APP).setCCategory(
            'rodos'
        )
    except BaseException:
        pass
    try:
        self.config.dtypes.otherprojection.type_extension(ELAN_APP).setCCategory(
            'other'
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
