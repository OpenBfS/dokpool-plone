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
        TITLE: 'Vorlage aktuelle Situation',
        ID: 'esd',
        CHILDREN: [
            {
                TYPE: 'Document',
                TITLE: u'Elektronische Lagedarstellung',
                ID: 'front-page',
                'text': FRONTPAGE,
                CHILDREN: [],
            }
        ],
    },
    {
        TYPE: 'ELANContentConfig',
        TITLE: 'Konfiguration Inhalte',
        ID: 'contentconfig',
        CHILDREN: [
            {TYPE: 'Text', TITLE: u'Impressum', ID: 'impressum', CHILDREN: []},
            {TYPE: 'Text', TITLE: u'Hilfe', ID: 'help', CHILDREN: []},
        ],
    },
]
DOCTYPES = (
    'ref_setDocTypesUpdateCollection'
)  # indicates that docTypes is referencing objects, which need to be queried by their id

ESDCOLLECTIONS = [
    {
        TYPE: 'ELANSection',
        TITLE: u'EREIGNIS',
        ID: 'incident',
        CHILDREN: [
            {
                TYPE: 'ELANDocCollection',
                TITLE: u'MELDUNGEN',
                ID: 'notifications',
                CHILDREN: [],
                DOCTYPES: ['notification', 'note'],
            },
            {
                TYPE: 'ELANDocCollection',
                TITLE: u'ANLAGENINFORMATION',
                ID: 'event-npp-information',
                CHILDREN: [],
                DOCTYPES: ['eventinformation', 'nppinformation'],
            },
        ],
    },
    {
        TYPE: 'ELANSection',
        TITLE: u'METEOROLOGIE',
        ID: 'meteorology',
        CHILDREN: [
            {
                TYPE: 'ELANDocCollection',
                TITLE: u'WETTERINFORMATION',
                ID: 'weather-information',
                CHILDREN: [],
                DOCTYPES: ['weatherinformation'],
            },
            {
                TYPE: 'ELANDocCollection',
                TITLE: u'TRAJEKTORIEN',
                ID: 'trajectories',
                CHILDREN: [],
                DOCTYPES: ['trajectory'],
            },
        ],
    },
    {
        TYPE: 'ELANSection',
        TITLE: u'PROGNOSEN',
        ID: 'dose-projections',
        CHILDREN: [
            {
                TYPE: 'ELANDocCollection',
                TITLE: u'PROGNOSEN-RODOS',
                ID: 'rodos-projections',
                CHILDREN: [],
                DOCTYPES: ['rodosprojection'],
            },
            {
                TYPE: 'ELANDocCollection',
                TITLE: u'PROGNOSEN LAND',
                ID: 'state-projections',
                CHILDREN: [],
                DOCTYPES: ['stateprojection'],
            },
            {
                TYPE: 'ELANDocCollection',
                TITLE: u'PROGNOSEN ANDERE',
                ID: 'other-projections',
                CHILDREN: [],
                DOCTYPES: ['otherprojection'],
            },
        ],
    },
    {
        TYPE: 'ELANSection',
        TITLE: u'MESSERGEBNISSE',
        ID: 'measurement-results',
        CHILDREN: [
            {
                TYPE: 'ELANDocCollection',
                TITLE: u'ODL',
                ID: 'gamma-dose-rate',
                CHILDREN: [],
                DOCTYPES: [
                    'gammadoserate',
                    'gammadoserate_timeseries',
                    'gammadoserate_mobile',
                ],
            },
            {
                TYPE: 'ELANDocCollection',
                TITLE: u'LUFTAKTIVITÄT',
                ID: 'air-activity',
                CHILDREN: [],
                DOCTYPES: ['airactivity'],
            },
            {
                TYPE: 'ELANDocCollection',
                TITLE: u'IN-SITU MESSUNGEN',
                ID: 'insitu',
                CHILDREN: [],
                DOCTYPES: ['mresult_insitu'],
            },
            {
                TYPE: 'ELANDocCollection',
                TITLE: u'BODENKONTAMINATION',
                ID: 'ground-contamination',
                CHILDREN: [],
                DOCTYPES: ['groundcontamination'],
            },
            {
                TYPE: 'ELANDocCollection',
                TITLE: u'LEBENS- UND FUTTERMITTEL',
                ID: 'food-and-feed',
                CHILDREN: [],
                DOCTYPES: ['mresult_feed', 'mresult_food'],
            },
            {
                TYPE: 'ELANDocCollection',
                TITLE: u'GEWÄSSER',
                ID: 'water',
                CHILDREN: [],
                DOCTYPES: ['mresult_water'],
            },
            {
                TYPE: 'ELANDocCollection',
                TITLE: u'SONSTIGE MESSUNGEN',
                ID: 'other',
                CHILDREN: [],
                DOCTYPES: ['mresult_other', 'mresult_flight'],
            },
        ],
    },
    {
        TYPE: 'ELANSection',
        TITLE: u'LAGE',
        ID: 'current-situation',
        CHILDREN: [
            {
                TYPE: 'ELANDocCollection',
                TITLE: u'LAGEBERICHTE',
                ID: 'situation-reports',
                CHILDREN: [],
                DOCTYPES: ['situationreport', 'sitrep'],
            },
            {
                TYPE: 'ELANDocCollection',
                TITLE: u'BEWERTUNG UND MASSNAHMEN',
                ID: 'protective-actions',
                CHILDREN: [],
                DOCTYPES: ['estimation', 'instructions', 'protectiveactions'],
            },
        ],
    },
    {
        TYPE: 'ELANSection',
        TITLE: u'INFORMATION DER ÖFFENTLICHKEIT',
        ID: 'information-of-the-public',
        CHILDREN: [
            {
                TYPE: 'ELANDocCollection',
                TITLE: u'PRESSEMITTEILUNGEN',
                ID: 'media-releases',
                CHILDREN: [],
                DOCTYPES: ['mediarelease'],
            }
        ],
    },
    {
        TYPE: 'ELANDocCollection',
        TITLE: 'Überblick',
        ID: 'overview',
        "setExcludeFromNav": True,
        DOCTYPES: [],
        CHILDREN: [],
    },
    {
        TYPE: 'ELANDocCollection',
        TITLE: 'Alle Dokumente',
        ID: 'recent',
        "setExcludeFromNav": True,
        DOCTYPES: [],
        CHILDREN: [],
    },
    {TYPE: 'Dashboard', TITLE: 'Pinnwand', ID: 'dashboard', "setExcludeFromNav": True},
    {
        TYPE: 'SituationOverview',
        TITLE: 'Lageübersicht',
        ID: 'situationoverview',
        "setExcludeFromNav": True,
    },
]

BASICSTRUCTURE2 = [
    {
        TYPE: 'ELANCurrentSituation',
        TITLE: 'Vorlage aktuelle Situation',
        ID: 'esd',
        CHILDREN: ESDCOLLECTIONS,
    }
]

# Structure definitions
# CHANGE HERE. DocTypes, DocCollections and their connections must match.

DTYPES = [
    {
        TYPE: 'DocType',
        TITLE: u'Meldung',
        ID: 'notification',
        CHILDREN: [],
        'local_behaviors': ['elan', 'doksys'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Mitteilung',
        ID: 'note',
        CHILDREN: [],
        'local_behaviors': ['elan', 'doksys'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Ereignisinformation',
        ID: 'eventinformation',
        CHILDREN: [],
        'local_behaviors': ['elan', 'doksys'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Anlageninformation',
        ID: 'nppinformation',
        CHILDREN: [],
        'local_behaviors': ['elan', 'doksys'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Wetterinformation',
        ID: 'weatherinformation',
        CHILDREN: [],
        'local_behaviors': ['elan', 'doksys'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Trajektorie',
        ID: 'trajectory',
        CHILDREN: [],
        'local_behaviors': ['elan', 'doksys'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'RODOS_Prognose',
        ID: 'rodosprojection',
        CHILDREN: [],
        'local_behaviors': ['elan', 'doksys'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Prognose_Land',
        ID: 'stateprojection',
        CHILDREN: [],
        'local_behaviors': ['elan', 'doksys'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Andere_Prognose',
        ID: 'otherprojection',
        CHILDREN: [],
        'local_behaviors': ['elan', 'doksys'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Messergebnis_ODL',
        ID: 'gammadoserate',
        CHILDREN: [],
        'local_behaviors': ['elan', 'doksys'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Messergebnis_ODL_Zeitreihe',
        ID: 'gammadoserate_timeseries',
        CHILDREN: [],
        'local_behaviors': ['elan', 'doksys'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Messergebnis_ODL_Messspur',
        ID: 'gammadoserate_mobile',
        CHILDREN: [],
        'local_behaviors': ['elan', 'doksys'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Messergebnis_Luftaktivität',
        ID: 'airactivity',
        CHILDREN: [],
        'local_behaviors': ['elan', 'doksys'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Messergebnis_insitu',
        ID: 'mresult_insitu',
        CHILDREN: [],
        'local_behaviors': ['elan', 'doksys'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Messergebnis_Bodenkontamination',
        ID: 'groundcontamination',
        CHILDREN: [],
        'local_behaviors': ['elan', 'doksys'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Messergebnis_Futtermittel',
        ID: 'mresult_feed',
        CHILDREN: [],
        'local_behaviors': ['elan', 'doksys'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Messergebnis_Lebensmittel',
        ID: 'mresult_food',
        CHILDREN: [],
        'local_behaviors': ['elan', 'doksys'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Messergebnis_Gewässer',
        ID: 'mresult_water',
        CHILDREN: [],
        'local_behaviors': ['elan', 'doksys'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Messergebnis_Sonstige',
        ID: 'mresult_other',
        CHILDREN: [],
        'local_behaviors': ['elan', 'doksys'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Messergebnis_Aerogamma',
        ID: 'mresult_flight',
        CHILDREN: [],
        'local_behaviors': ['elan', 'doksys'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Lageinformation',
        ID: 'situationreport',
        CHILDREN: [],
        'local_behaviors': ['elan', 'doksys'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Lagebericht',
        ID: 'sitrep',
        CHILDREN: [],
        'local_behaviors': ['elan', 'doksys'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Bewertung',
        ID: 'estimation',
        CHILDREN: [],
        'local_behaviors': ['elan', 'doksys'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Maßnahmeninformation',
        ID: 'instructions',
        CHILDREN: [],
        'local_behaviors': ['elan', 'doksys'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Maßnahmenempfehlungen',
        ID: 'protectiveactions',
        CHILDREN: [],
        'local_behaviors': ['elan', 'doksys'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Pressemitteilung',
        ID: 'mediarelease',
        CHILDREN: [],
        'local_behaviors': ['elan', 'doksys'],
    },
    {
        TYPE: 'DocType',
        TITLE: u'Insitu_Information',
        ID: 'insituinformation',
        CHILDREN: [],
        'local_behaviors': ['elan', 'doksys'],
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
    except Exception, e:
        log_exc(e)
    try:
        self.config.dtypes.note.type_extension(ELAN_APP).setCCategory('notifications')
    except:
        pass
    try:
        self.config.dtypes.eventinformation.type_extension(ELAN_APP).setCCategory(
            'event-npp-information'
        )
    except:
        pass
    try:
        self.config.dtypes.nppinformation.type_extension(ELAN_APP).setCCategory(
            'event-npp-information'
        )
    except:
        pass
    try:
        self.config.dtypes.weatherinformation.type_extension(ELAN_APP).setCCategory(
            'weather-information'
        )
    except:
        pass
    try:
        self.config.dtypes.trajectory.type_extension(ELAN_APP).setCCategory(
            'trajectories'
        )
    except:
        pass
    try:
        self.config.dtypes.nppprojection.type_extension(ELAN_APP).setCCategory(
            'npp-projections'
        )
    except:
        pass
    try:
        self.config.dtypes.rodosprojection.type_extension(ELAN_APP).setCCategory(
            'rodos'
        )
    except:
        pass
    try:
        self.config.dtypes.otherprojection.type_extension(ELAN_APP).setCCategory(
            'other'
        )
    except:
        pass
    try:
        self.config.dtypes.gammadoserate.type_extension(ELAN_APP).setCCategory(
            'gamma-dose-rate'
        )
    except:
        pass
    try:
        self.config.dtypes.airactivity.type_extension(ELAN_APP).setCCategory(
            'air-activity'
        )
    except:
        pass
    try:
        self.config.dtypes.groundcontamination.type_extension(ELAN_APP).setCCategory(
            'ground-contamination'
        )
    except:
        pass
    try:
        self.config.dtypes.mresult_feed.type_extension(ELAN_APP).setCCategory(
            'food-and-feed'
        )
    except:
        pass
    try:
        self.config.dtypes.mresult_food.type_extension(ELAN_APP).setCCategory(
            'food-and-feed'
        )
    except:
        pass
    try:
        self.config.dtypes.mresult_water.type_extension(ELAN_APP).setCCategory('water')
    except:
        pass
    try:
        self.config.dtypes.situationreport.type_extension(ELAN_APP).setCCategory(
            'situation-reports'
        )
    except:
        pass
    try:
        self.config.dtypes.sitrep.type_extension(ELAN_APP).setCCategory(
            'situation-reports'
        )
    except:
        pass
    try:
        self.config.dtypes.protectiveactions.type_extension(ELAN_APP).setCCategory(
            'protective-actions'
        )
    except:
        pass
    try:
        self.config.dtypes.mediarelease.type_extension(ELAN_APP).setCCategory(
            'media-releases'
        )
    except:
        pass
    try:
        self.config.dtypes.instructions.type_extension(ELAN_APP).setCCategory(
            'instructions-to-the-public'
        )
    except:
        pass
