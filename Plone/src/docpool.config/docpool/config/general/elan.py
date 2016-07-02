# -*- coding: utf-8 -*-
from docpool.elan.config import ELAN_APP
from docpool.config.utils import ID, TYPE, TITLE, CHILDREN, createPloneObjects
from docpool.transfers.config import TRANSFERS_APP
from Products.CMFCore.utils import getToolByName
from plone.app.textfield.value import RichTextValue
from docpool.base.events import IDocumentPoolUndeleteable
from Products.Five.utilities.marker import mark
import transaction

def install(self):
    """
    """
    fresh = True
    if self.hasObject("esd"):
        fresh = False # It's a reinstall
    configUsers(self, fresh)
    createStructure(self, fresh)
    if fresh:
        connectTypesAndCategories(self)
    setFrontpage(self)

def configUsers(self, fresh):
    """
    """
    mtool = getToolByName(self, "portal_membership")
    if fresh:
        mtool.addMember('elanadmin', 'ELAN Administrator (global)', ['Site Administrator', 'Member'], [])
        elanadmin = mtool.getMemberById('elanadmin')
        elanadmin.setMemberProperties(
            {"fullname": 'ELAN Administrator'})
        elanadmin.setSecurityProfile(password="admin")
        mtool.addMember('elanmanager', 'ELAN Manager (global)', ['Manager', 'Member'], [])
        elanmanager = mtool.getMemberById('elanmanager')
        elanmanager.setMemberProperties(
            {"fullname": 'ELAN Manager'})
        elanmanager.setSecurityProfile(password="admin")

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

BASICSTRUCTURE = [{TYPE: 'ELANCurrentSituation', TITLE: 'Current Situation Template', ID: 'esd', CHILDREN: [
    {TYPE: 'Document', TITLE: u'Electronic Situation Display', ID: 'front-page', 'text': FRONTPAGE, CHILDREN: []},
]},
{TYPE: 'ELANContentConfig', TITLE: 'Content Configuration', ID: 'contentconfig', CHILDREN: [
    {TYPE: 'Text', TITLE: u'Impressum', ID: 'impressum', CHILDREN: []},
    {TYPE: 'Text', TITLE: u'Help', ID: 'help', CHILDREN: []},
]},
                  ]
DOCTYPES = 'ref_setDocTypesUpdateCollection'  # indicates that docTypes is referencing objects, which need to be queried by their id

ESDCOLLECTIONS = [{TYPE: 'ELANSection', TITLE: u'INCIDENT', ID: 'incident', CHILDREN: [
    {TYPE: 'ELANDocCollection', TITLE: u'NOTIFICATIONS', ID: 'notifications', CHILDREN: [], DOCTYPES: ['notification']},
    {TYPE: 'ELANDocCollection', TITLE: u'EVENT / NPP INFORMATION', ID: 'event-npp-information', CHILDREN: [],
     DOCTYPES: ['eventinformation', 'nppinformation']},
]},
                  {TYPE: 'ELANSection', TITLE: u'METEOROLOGY', ID: 'meteorology', CHILDREN: [
                      {TYPE: 'ELANDocCollection', TITLE: u'WEATHER INFORMATION', ID: 'weather-information',
                       CHILDREN: [], DOCTYPES: ['weatherinformation']},
                      {TYPE: 'ELANDocCollection', TITLE: u'TRAJECTORIES', ID: 'trajectories', CHILDREN: [],
                       DOCTYPES: ['trajectory']},
                  ]},
                  {TYPE: 'ELANSection', TITLE: u'DOSE PROJECTIONS', ID: 'dose-projections', CHILDREN: [
                      {TYPE: 'ELANDocCollection', TITLE: u'CNCAN PROJECTIONS', ID: 'cncan-projections', CHILDREN: [],
                       DOCTYPES: ['cncanprojection']},
                      {TYPE: 'ELANDocCollection', TITLE: u'IFIN PROJECTIONS', ID: 'ifin-projections', CHILDREN: [],
                       DOCTYPES: ['ifinprojection']},
                      {TYPE: 'ELANDocCollection', TITLE: u'NPP PROJECTIONS', ID: 'npp-projections', CHILDREN: [],
                       DOCTYPES: ['nppprojection']},
                      {TYPE: 'ELANDocCollection', TITLE: u'RODOS', ID: 'rodos', CHILDREN: [],
                       DOCTYPES: ['rodosprojection']},
                      {TYPE: 'ELANDocCollection', TITLE: u'OTHER', ID: 'other', CHILDREN: [],
                       DOCTYPES: ['otherprojection']},
                  ]},
                  {TYPE: 'ELANSection', TITLE: u'MEASUREMENT RESULTS', ID: 'measurement-results', CHILDREN: [
                      {TYPE: 'ELANDocCollection', TITLE: u'GAMMA DOSE RATE', ID: 'gamma-dose-rate', CHILDREN: [],
                       DOCTYPES: ['gammadoserate']},
                      {TYPE: 'ELANDocCollection', TITLE: u'AIR ACTIVITY', ID: 'air-activity', CHILDREN: [],
                       DOCTYPES: ['airactivity']},
                      {TYPE: 'ELANDocCollection', TITLE: u'GROUND CONTAMINATION', ID: 'ground-contamination',
                       CHILDREN: [], DOCTYPES: ['groundcontamination']},
                      {TYPE: 'ELANDocCollection', TITLE: u'FOOD AND FEED', ID: 'food-and-feed', CHILDREN: [],
                       DOCTYPES: ['mresult_feed', 'mresult_food']},
                      {TYPE: 'ELANDocCollection', TITLE: u'WATER', ID: 'water', CHILDREN: [],
                       DOCTYPES: ['mresult_water']},
                  ]},
                  {TYPE: 'ELANSection', TITLE: u'CURRENT SITUATION', ID: 'current-situation', CHILDREN: [
                      {TYPE: 'ELANDocCollection', TITLE: u'SITUATION REPORTS', ID: 'situation-reports', CHILDREN: [],
                       DOCTYPES: ['nppinformation', 'situationreport']},
                      {TYPE: 'ELANDocCollection', TITLE: u'PROTECTIVE ACTIONS', ID: 'protective-actions', CHILDREN: [],
                       DOCTYPES: ['instructions', 'protectiveactions']},
                  ]},
                  {TYPE: 'ELANSection', TITLE: u'INFORMATION OF THE PUBLIC', ID: 'information-of-the-public',
                   CHILDREN: [
                       {TYPE: 'ELANDocCollection', TITLE: u'MEDIA RELEASES', ID: 'media-releases', CHILDREN: [],
                        DOCTYPES: ['mediarelease']},
                       {TYPE: 'ELANDocCollection', TITLE: u'INSTRUCTIONS TO THE PUBLIC',
                        ID: 'instructions-to-the-public', CHILDREN: [], DOCTYPES: ['instructions']},
                   ]},
                  {TYPE: 'ELANDocCollection', TITLE: 'Overview', ID: 'overview', "setExcludeFromNav": True,
                   DOCTYPES: [], CHILDREN: []},
                  {TYPE: 'ELANDocCollection', TITLE: 'All documents', ID: 'recent', "setExcludeFromNav": True,
                   DOCTYPES: [], CHILDREN: []},
                  {TYPE: 'Dashboard', TITLE: 'Dashboard', ID: 'dashboard', "setExcludeFromNav": True},
                  ]

BASICSTRUCTURE2 = [
    {TYPE: 'ELANCurrentSituation', TITLE: 'Current Situation Template', ID: 'esd', CHILDREN: ESDCOLLECTIONS},
    ]

# Structure definitions
# CHANGE HERE. DocTypes, DocCollections and their connections must match.

DTYPES = [{TYPE: 'DocType', TITLE: u'Event Information', ID: 'eventinformation',
           CHILDREN: [{TYPE: 'ELANType', TITLE: 'ELANType', ID: ELAN_APP},
                      {TYPE: 'TransfersType', TITLE: 'TransfersType', ID: TRANSFERS_APP}]},
          {TYPE: 'DocType', TITLE: u'Notification', ID: 'notification',
           CHILDREN: [{TYPE: 'ELANType', TITLE: 'ELANType', ID: ELAN_APP},
                      {TYPE: 'TransfersType', TITLE: 'TransfersType', ID: TRANSFERS_APP}]},
          {TYPE: 'DocType', TITLE: u'NPP Information', ID: 'nppinformation',
           CHILDREN: [{TYPE: 'ELANType', TITLE: 'ELANType', ID: ELAN_APP},
                      {TYPE: 'TransfersType', TITLE: 'TransfersType', ID: TRANSFERS_APP}]},
          {TYPE: 'DocType', TITLE: u'Weather Information', ID: 'weatherinformation',
           CHILDREN: [{TYPE: 'ELANType', TITLE: 'ELANType', ID: ELAN_APP},
                      {TYPE: 'TransfersType', TITLE: 'TransfersType', ID: TRANSFERS_APP}]},
          {TYPE: 'DocType', TITLE: u'Trajectory', ID: 'trajectory',
           CHILDREN: [{TYPE: 'ELANType', TITLE: 'ELANType', ID: ELAN_APP},
                      {TYPE: 'TransfersType', TITLE: 'TransfersType', ID: TRANSFERS_APP}]},
          {TYPE: 'DocType', TITLE: u'CNCAN Projection', ID: 'cncanprojection',
           CHILDREN: [{TYPE: 'ELANType', TITLE: 'ELANType', ID: ELAN_APP},
                      {TYPE: 'TransfersType', TITLE: 'TransfersType', ID: TRANSFERS_APP}]},
          {TYPE: 'DocType', TITLE: u'IFIN Projection', ID: 'ifinprojection',
           CHILDREN: [{TYPE: 'ELANType', TITLE: 'ELANType', ID: ELAN_APP},
                      {TYPE: 'TransfersType', TITLE: 'TransfersType', ID: TRANSFERS_APP}]},
          {TYPE: 'DocType', TITLE: u'NPP Projection', ID: 'nppprojection',
           CHILDREN: [{TYPE: 'ELANType', TITLE: 'ELANType', ID: ELAN_APP},
                      {TYPE: 'TransfersType', TITLE: 'TransfersType', ID: TRANSFERS_APP}]},
          {TYPE: 'DocType', TITLE: u'RODOS Projection', ID: 'rodosprojection',
           CHILDREN: [{TYPE: 'ELANType', TITLE: 'ELANType', ID: ELAN_APP},
                      {TYPE: 'TransfersType', TITLE: 'TransfersType', ID: TRANSFERS_APP}]},
          {TYPE: 'DocType', TITLE: u'Other Projection', ID: 'otherprojection',
           CHILDREN: [{TYPE: 'ELANType', TITLE: 'ELANType', ID: ELAN_APP},
                      {TYPE: 'TransfersType', TITLE: 'TransfersType', ID: TRANSFERS_APP}]},
          {TYPE: 'DocType', TITLE: u'Gamma Dose Rate', ID: 'gammadoserate',
           CHILDREN: [{TYPE: 'ELANType', TITLE: 'ELANType', ID: ELAN_APP},
                      {TYPE: 'TransfersType', TITLE: 'TransfersType', ID: TRANSFERS_APP}]},
          {TYPE: 'DocType', TITLE: u'Air Activity', ID: 'airactivity',
           CHILDREN: [{TYPE: 'ELANType', TITLE: 'ELANType', ID: ELAN_APP},
                      {TYPE: 'TransfersType', TITLE: 'TransfersType', ID: TRANSFERS_APP}]},
          {TYPE: 'DocType', TITLE: u'Ground Contamination', ID: 'groundcontamination',
           CHILDREN: [{TYPE: 'ELANType', TITLE: 'ELANType', ID: ELAN_APP},
                      {TYPE: 'TransfersType', TITLE: 'TransfersType', ID: TRANSFERS_APP}]},
          {TYPE: 'DocType', TITLE: u'Measurement Result Feed', ID: 'mresult_feed',
           CHILDREN: [{TYPE: 'ELANType', TITLE: 'ELANType', ID: ELAN_APP},
                      {TYPE: 'TransfersType', TITLE: 'TransfersType', ID: TRANSFERS_APP}]},
          {TYPE: 'DocType', TITLE: u'Measurement Result Food', ID: 'mresult_food',
           CHILDREN: [{TYPE: 'ELANType', TITLE: 'ELANType', ID: ELAN_APP},
                      {TYPE: 'TransfersType', TITLE: 'TransfersType', ID: TRANSFERS_APP}]},
          {TYPE: 'DocType', TITLE: u'Measurement Result Water', ID: 'mresult_water',
           CHILDREN: [{TYPE: 'ELANType', TITLE: 'ELANType', ID: ELAN_APP},
                      {TYPE: 'TransfersType', TITLE: 'TransfersType', ID: TRANSFERS_APP}]},
          {TYPE: 'DocType', TITLE: u'Situation Report', ID: 'situationreport',
           CHILDREN: [{TYPE: 'ELANType', TITLE: 'ELANType', ID: ELAN_APP},
                      {TYPE: 'TransfersType', TITLE: 'TransfersType', ID: TRANSFERS_APP}]},
          {TYPE: 'DocType', TITLE: u'Instructions to the Public', ID: 'instructions',
           CHILDREN: [{TYPE: 'ELANType', TITLE: 'ELANType', ID: ELAN_APP},
                      {TYPE: 'TransfersType', TITLE: 'TransfersType', ID: TRANSFERS_APP}]},
          {TYPE: 'DocType', TITLE: u'Protective Actions', ID: 'protectiveactions',
           CHILDREN: [{TYPE: 'ELANType', TITLE: 'ELANType', ID: ELAN_APP},
                      {TYPE: 'TransfersType', TITLE: 'TransfersType', ID: TRANSFERS_APP}]},
          {TYPE: 'DocType', TITLE: u'Media Release', ID: 'mediarelease',
           CHILDREN: [{TYPE: 'ELANType', TITLE: 'ELANType', ID: ELAN_APP},
                      {TYPE: 'TransfersType', TITLE: 'TransfersType', ID: TRANSFERS_APP}]},
          ]



def connectTypesAndCategories(self):
    """
    """
    try:
        self.config.dtypes.eventinformation.extension(ELAN_APP).setCCategory('event-npp-information')
    except:
        pass
    try:
        self.config.dtypes.weatherinformation.extension(ELAN_APP).setCCategory('weather-information')
    except:
        pass
    try:
        self.config.dtypes.trajectory.extension(ELAN_APP).setCCategory('trajectories')
    except:
        pass
    try:
        self.config.dtypes.cncanprojection.extension(ELAN_APP).setCCategory('cncan-projections')
    except:
        pass
    try:
        self.config.dtypes.ifinprojection.extension(ELAN_APP).setCCategory('ifin-projections')
    except:
        pass
    try:
        self.config.dtypes.nppprojection.extension(ELAN_APP).setCCategory('npp-projections')
    except:
        pass
    try:
        self.config.dtypes.rodosprojection.extension(ELAN_APP).setCCategory('rodos')
    except:
        pass
    try:
        self.config.dtypes.otherprojection.extension(ELAN_APP).setCCategory('other')
    except:
        pass
    try:
        self.config.dtypes.gammadoserate.extension(ELAN_APP).setCCategory('gamma-dose-rate')
    except:
        pass
    try:
        self.config.dtypes.airactivity.extension(ELAN_APP).setCCategory('air-activity')
    except:
        pass
    try:
        self.config.dtypes.groundcontamination.extension(ELAN_APP).setCCategory('ground-contamination')
    except:
        pass
    try:
        self.config.dtypes.mresult_feed.extension(ELAN_APP).setCCategory('food-and-feed')
    except:
        pass
    try:
        self.config.dtypes.mresult_food.extension(ELAN_APP).setCCategory('food-and-feed')
    except:
        pass
    try:
        self.config.dtypes.mresult_water.extension(ELAN_APP).setCCategory('water')
    except:
        pass
    try:
        self.config.dtypes.situationreport.extension(ELAN_APP).setCCategory('situation-reports')
    except:
        pass
    try:
        self.config.dtypes.protectiveactions.extension(ELAN_APP).setCCategory('protective-actions')
    except:
        pass
    try:
        self.config.dtypes.mediarelease.extension(ELAN_APP).setCCategory('media-releases')
    except:
        pass
    try:
        self.config.dtypes.instructions.extension(ELAN_APP).setCCategory('instructions-to-the-public')
    except:
        pass
    try:
        self.config.dtypes.notification.extension(ELAN_APP).setCCategory('notifications')
    except:
        pass
    try:
        self.config.dtypes.nppinformation.extension(ELAN_APP).setCCategory('event-npp-information')
    except:
        pass
