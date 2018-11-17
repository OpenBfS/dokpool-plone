# -*- coding: utf-8 -*-
from docpool.config.utils import ID, TYPE, TITLE, CHILDREN, createPloneObjects
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.utils import shasattr
import transaction
from zExceptions import BadRequest
from Products.CMFPlone.utils import log_exc
from docpool.config.local.base import CONTENT_AREA
from docpool.config import _
from datetime import datetime
from docpool.config.general.elan import connectTypesAndCategories

# ELAN specific structures

def dpAdded(self):
    """
    """
    fresh = True
    if self.hasObject("esd"):
        fresh = False # It's a reinstall
    copyCurrentSituation(self, fresh)
    transaction.commit()
    createBasicPortalStructure(self, fresh)
    transaction.commit()
    createContentConfig(self, fresh)
    transaction.commit()
    if fresh:
        self.esd.correctAllDocTypes()
        transaction.commit()
        connectTypesAndCategories(self)

        placeful_wf = getToolByName(self, 'portal_placeful_workflow')
        try:
            self.archive.manage_addProduct['CMFPlacefulWorkflow'].manage_addWorkflowPolicyConfig()
        except BadRequest, e:
            # print type(e)
            log_exc(e)
        config = placeful_wf.getWorkflowPolicyConfig(self.archive)
        placefulWfName = 'elan-archive'
        config.setPolicyIn(policy=placefulWfName, update_security=False)
        config.setPolicyBelow(policy=placefulWfName, update_security=False)
        createELANUsers(self)
        createELANGroups(self)
        setELANLocalRoles(self)
        self.reindexAll()


BASICSTRUCTURE = [
    {TYPE: 'ELANArchives', TITLE: u'Archive', ID: 'archive', CHILDREN: []},
]

ARCHIVESTRUCTURE = [{TYPE: 'ELANCurrentSituation', TITLE: 'Elektronische Lagedarstellung', ID: 'esd', CHILDREN: []},
                    CONTENT_AREA,
                    ]

ADMINSTRUCTURE = [
    {TYPE: 'ELANContentConfig', TITLE: 'Konfiguration Inhalte', ID: 'contentconfig', CHILDREN: [
        {TYPE: 'ELANScenarios', TITLE: u'Ereignisse', ID: 'scen', CHILDREN: [
            {TYPE: 'ELANScenario', TITLE: u'Normalfall', ID: 'routinemode', "status": "active",
             "timeOfEvent": datetime.now(), CHILDREN: []}
        ]},
        {TYPE: 'Text', TITLE: u'Ticker', ID: 'ticker', CHILDREN: []},
        {TYPE: 'Text', TITLE: u'Impressum', ID: 'impressum', CHILDREN: []},
        {TYPE: 'DashboardsConfig', TITLE: u'Dokumentsammlungen Pinnwand', ID: 'dbconfig', CHILDREN: []},
        {TYPE: 'IRIXConfig', TITLE: u'Konfiguration IRIX', ID: 'irix',
         'organisationReporting': 'www.yourorganisation.org',
         'contactName': 'Your Contact Name',
         'contactEmail': 'contact@yourorganisation.org',
         'organisationName': 'Your Organisation',
         'organisationId': 'www.yourorganisation.org',
         'organisationCountry': 'DE',
         'organisationWeb': 'http://www.yourorganisation.org',
         'organisationEmail': 'info@yourorganisation.org',
         'sourceText': 'ELAN-E Electronic Situation Display',
         'sourceDescription': 'http://elan.yourorganisation.org',
         'typeMapping': ('Event Information:Event information',
                         'Notification:Event information',
                         'Situation Report:Event information',
                         'NPP Information:Plant status',
                         'Weather Information:Meteorology',
                         'Gamma Dose Rate:Measurements',
                         'Air Activity:Measurements',
                         'Ground Contamination:Measurements',
                         'Measurement Result Food:Measurements',
                         'Measurement Result Feed:Measurements',
                         'Measurement Result Water:Measurements',
                         'Protective Actions:Protective actions',
                         'Instructions to the Public:Public information',
                         'Media Release:Public information - Press release',
                         'NPP Projection:Model result',
                         'RODOS Projection:Model result',
                         'Other Projection:Model result',
                         'Trajectory:Model result - Plume trajectory'),

         CHILDREN: [],}
    ]}]



def createBasicPortalStructure(plonesite, fresh):
    """
    """
    createPloneObjects(plonesite, BASICSTRUCTURE, fresh)


def createContentConfig(plonesite, fresh):
    """
    """
    createPloneObjects(plonesite, ADMINSTRUCTURE, fresh)


def createELANUsers(self):
    # Set type for user folders
    mtool = getToolByName(self, "portal_membership")
    prefix = self.prefix or self.getId()
    prefix = str(prefix)
    title = self.Title()
    mtool.addMember('%s_elanadmin' % prefix, 'ELAN Administrator (%s)' % title, ['Member'], [])
    elanadmin = mtool.getMemberById('%s_elanadmin' % prefix)
    elanadmin.setMemberProperties(
        {"fullname": 'ELAN Administrator (%s)' % title,
         "dp": self.UID()})
    elanadmin.setSecurityProfile(password="admin")
    mtool.addMember('%s_contentadmin' % prefix, 'Content Admin (%s)' % title, ['Member'], [])
    contentadmin = mtool.getMemberById('%s_contentadmin' % prefix)
    contentadmin.setMemberProperties(
        {"fullname": 'Content Admin (%s)' % title,
         "dp": self.UID()})
    contentadmin.setSecurityProfile(password="admin")


def setELANLocalRoles(self):
    """
    Normal local members: Reader
    Administrators: Site Administrator
    ContentAdministrators: Reviewer
    Receivers: Owner, Editor
    Senders: Contributor
    """
    prefix = self.prefix or self.getId()
    prefix = str(prefix)
    self.contentconfig.manage_setLocalRoles("%s_ContentAdministrators" % prefix, ["ContentAdmin"])
    self.archive.manage_setLocalRoles("%s_ContentAdministrators" % prefix, ["DocPoolAdmin"])
    self.content.Groups.manage_setLocalRoles("%s_ContentAdministrators" % prefix, ["Site Administrator"])
    self.esd.manage_setLocalRoles("%s_ContentAdministrators" % prefix, ["ContentAdmin"])
    self.manage_setLocalRoles("%s_ELANUsers" % prefix, ["ELANUser"])
    self.config.manage_setLocalRoles("%s_ContentAdministrators" % prefix, ["Owner"])


def createELANGroups(self):
    # We need local groups for
    # - General access to the ESD
    # - Administration
    # - Content Administration
    # - Receiving content from others
    # - Sending content to others

    prefix = self.prefix or self.getId()
    prefix = str(prefix)
    title = self.Title()
    gtool = getToolByName(self, 'portal_groups')
    gtool.addPrincipalToGroup('%s_elanadmin' % prefix, '%s_Members' % prefix)
    gtool.addPrincipalToGroup('%s_contentadmin' % prefix, '%s_Members' % prefix)
    gtool.addPrincipalToGroup('%s_elanadmin' % prefix, '%s_Administrators' % prefix)
    # Content administrator group
    props = {'allowedDocTypes': [], 'title': 'Content Administrators (%s)' % title,
             'description': 'Responsible for the definition of scenarios, ticker texts and additional content.',
             'dp': self.UID()}
    gtool.addGroup("%s_ContentAdministrators" % prefix,
                   properties=props)
    gtool.addPrincipalToGroup('%s_contentadmin' % prefix, '%s_ContentAdministrators' % prefix)
    # Group for ELAN application rights
    props = {'allowedDocTypes': [], 'title': 'ELAN Users (%s)' % title,
             'description': 'Users with access to ELAN functions.',
             'dp': self.UID()}
    gtool.addGroup("%s_ELANUsers" % prefix,
               properties=props)
    gtool.addPrincipalToGroup('%s_elanadmin' % prefix, '%s_ELANUsers' % prefix)
    gtool.addPrincipalToGroup('%s_contentadmin' % prefix, '%s_ELANUsers' % prefix)
    gtool.addPrincipalToGroup('%s_dpadmin' % prefix, '%s_ELANUsers' % prefix)


def copyCurrentSituation(self, fresh):
    """
    """
    if not fresh:
        return
    esd = self.esd
    from docpool.base.utils import _copyPaste
    _copyPaste(esd, self, safe=False)
    self.esd.setTitle(_("Aktuelle Lage"))
    self.esd.reindexObject()
    # make sure the current situation is first
    self.moveObject("esd", 0)

def dpRemoved(self):
    """
    @param self:
    @return:
    """
    return
