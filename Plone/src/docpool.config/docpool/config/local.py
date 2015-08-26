# -*- coding: utf-8 -*-
from docpool.config.utils import ID, TYPE, TITLE, CHILDREN, createPloneObjects
from Products.CMFCore.utils import getToolByName
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from Products.Archetypes.utils import shasattr
import transaction
from zExceptions import BadRequest
from Products.CMFPlone.utils import log_exc
from docpool.config.general import DOCTYPES
from docpool.config import _
# General Docpool structures

CONTENT_AREA = {TYPE: 'ContentArea', TITLE: u'Content Area', ID: 'content', "setExcludeFromNav": True, CHILDREN: [
                    {TYPE: 'Users', TITLE: u'Members', ID: 'Members', CHILDREN: []},                                                                                              
                    {TYPE: 'Groups', TITLE: u'Groups', ID: 'Groups', CHILDREN: []},                                                                                              
                                                                                              ]}


def createContentArea(self, fresh):
    """
    """
    createPloneObjects(self, [ CONTENT_AREA ], fresh)
    

def createUsers(self):    
    # Set type for user folders
    mtool = getToolByName(self,"portal_membership")
    prefix = self.prefix or self.getId()
    prefix = str(prefix)
    title = self.Title()
    mtool.addMember('%s_dpadmin' % prefix, 'DocPool Administrator (%s)' % title, ['Member'], [])
    dpadmin = mtool.getMemberById('%s_dpadmin' % prefix)
    dpadmin.setMemberProperties(
        {"fullname": 'DocPool Administrator (%s)' % title,
         "dp": self.UID()})
    dpadmin.setSecurityProfile(password="admin")
    
def setLocalRoles(self):
    """
    Normal local members: Reader
    Administrators: Site Administrator
    ContentAdministrators: Reviewer
    Receivers: Owner, Editor
    Senders: Contributor
    """
    prefix = self.prefix or self.getId()
    prefix = str(prefix)
    self.manage_setLocalRoles("%s_Members" % prefix, ["Reader"])
    self.manage_setLocalRoles("%s_Administrators" % prefix, ["Site Administrator"])

def createGroups(self):
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
    props = { 'allowedDocTypes' : [], 'title' : 'Members (%s)' % title, 'description': 'Users of the DocPool.', 'dp': self.UID() }
    gtool.addGroup("%s_Members" % prefix, 
                   properties=props)
    gtool.addPrincipalToGroup('%s_dpadmin' % prefix, '%s_Members' % prefix)
    props = { 'allowedDocTypes' : [], 'title' : 'Administrators (%s)' % title, 'description': 'Responsible for the administration of the DocPool.', 'dp': self.UID() }
    gtool.addGroup("%s_Administrators" % prefix, 
                   properties=props)
    gtool.addPrincipalToGroup('%s_dpadmin' % prefix, '%s_Administrators' % prefix)

def navSettings(self):    
    IExcludeFromNavigation(self.content).exclude_from_nav = True
    self.content.reindexObject()    
    
# ELAN specific structures

TRANSFER_AREA = [
                    {TYPE: 'ELANTransfers', TITLE: u'Transfers', ID: 'Transfers', CHILDREN: []},                                                                                                                                                                                            
               ]
                            
BASICSTRUCTURE = [
                  {TYPE: 'ELANArchives', TITLE: u'Archive', ID: 'archive', CHILDREN: []},
                  ]


ARCHIVESTRUCTURE =  [ {TYPE: 'ELANCurrentSituation', TITLE: 'Electronic Situation Display', ID: 'esd', CHILDREN: []},
                      CONTENT_AREA,
                    ]   

ADMINSTRUCTURE = [
                  {TYPE: 'ELANContentConfig', TITLE: 'Content Configuration', ID: 'contentconfig', CHILDREN: [
                         {TYPE: 'ELANScenarios', TITLE: u'Scenarios', ID: 'scen', CHILDREN: [
                                 {TYPE: 'ELANScenario', TITLE: u'Routine mode', ID: 'routinemode', "status": "active", CHILDREN:[] }                                                            
                                                                                             ]},                                                            
                        {TYPE: 'Text', TITLE: u'Ticker', ID: 'ticker', CHILDREN: []},
                        {TYPE: 'Text', TITLE: u'Impressum', ID: 'impressum', CHILDREN: []},
                        {TYPE: 'IRIXConfig', TITLE: u'IRIX Configuration', ID: 'irix', 
                         'organisationReporting':'www.yourorganisation.org',
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
                                            'IFIN Projection:Model result', 
                                            'RODOS Projection:Model result', 
                                            'Other Projection:Model result', 
                                            'CNCAN Projection:Model result', 
                                            'Trajectory:Model result - Plume trajectory'),
                 
                         CHILDREN: [],}                                                         
                 ]}]


def createELANStructure(self, fresh):
    copyCurrentSituation(self, fresh)
    transaction.commit()
    createBasicPortalStructure(self, fresh)
    transaction.commit()
    createContentConfig(self,fresh)
    transaction.commit()
    copyDocTypes(self, fresh)
    self.esd.correctAllDocTypes()
    transaction.commit()
    placeful_wf = getToolByName(self, 'portal_placeful_workflow')
    try:
        self.archive.manage_addProduct['CMFPlacefulWorkflow'].manage_addWorkflowPolicyConfig()
    except BadRequest, e:
        #print type(e)
        log_exc(e)
    config = placeful_wf.getWorkflowPolicyConfig(self.archive)
    placefulWfName = 'elan-archive'
    config.setPolicyIn(policy=placefulWfName, update_security=False)
    config.setPolicyBelow(policy=placefulWfName, update_security=False)

def createDocTypes(plonesite, fresh):
    """
    """
    createPloneObjects(plonesite, ADMINSTRUCTURE, fresh)

def createBasicPortalStructure(plonesite, fresh):
    """
    """
    createPloneObjects(plonesite, BASICSTRUCTURE, fresh)

def copyDocTypes(self, fresh):
    """
    """
    if shasattr(self, "config"):
        return
    config = self.config
    from docpool.base.utils import _copyPaste
    _copyPaste(config, self)
    self.config.setTitle(_("Document Types"))
    self.config.reindexObject()

def createContentConfig(plonesite, fresh):
    """
    """
    createPloneObjects(plonesite, ADMINSTRUCTURE, fresh)

def createELANUsers(self):    
    # Set type for user folders
    mtool = getToolByName(self,"portal_membership")
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
    self.contentconfig.manage_setLocalRoles("%s_ContentAdministrators" % prefix, ["Reviewer"])
    self.content.Transfers.manage_setLocalRoles("%s_Receivers" % prefix, ["Owner"])
    self.esd.manage_setLocalRoles("%s_Receivers" % prefix, ["Reviewer"])
    self.content.Transfers.manage_setLocalRoles("%s_Administrators" % prefix, ["Owner"])
    self.contentconfig.scen.manage_setLocalRoles("%s_Receivers" % prefix, ["Editor"])
    self.config.manage_setLocalRoles("%s_Receivers" % prefix, ["Editor"])
    self.content.Groups.manage_setLocalRoles("%s_Senders" % prefix, ["Contributor"])

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
    props = { 'allowedDocTypes' : [], 'title' : 'Content Administrators (%s)' % title, 'description': 'Responsible for the definition of scenarios, ticker texts and additional content.', 'dp': self.UID() }
    gtool.addGroup("%s_ContentAdministrators" % prefix, 
                   properties=props)
    gtool.addPrincipalToGroup('%s_contentadmin' % prefix, '%s_ContentAdministrators' % prefix)
    props = { 'allowedDocTypes' : [], 'title' : 'Content Receivers (%s)' % title, 'description': 'Responsible for publishing content received from other ESDs.', 'dp': self.UID() }
    gtool.addGroup("%s_Receivers" % prefix, 
                   properties=props)
    props = { 'allowedDocTypes' : [], 'title' : 'Content Senders (%s)' % title, 'description': 'Responsible for sending content to other ESDs - if allowed by them.', 'dp': self.UID() }    
    gtool.addGroup("%s_Senders" % prefix, 
                   properties=props)

def copyCurrentSituation(self, fresh):
    """
    """
    if shasattr(self, "esd"):
        return
    esd = self.esd
    from docpool.base.utils import _copyPaste
    _copyPaste(esd, self)
    self.esd.setTitle(_("Situation Display"))
    self.esd.reindexObject()
    

def createTransferArea(self, fresh):
    """
    """
    createPloneObjects(self.content, TRANSFER_AREA, fresh)
    placeful_wf = getToolByName(self, 'portal_placeful_workflow')
    try:
        self.content.Transfers.manage_addProduct['CMFPlacefulWorkflow'].manage_addWorkflowPolicyConfig()
    except BadRequest, e:
        #print type(e)
        log_exc(e)
    config = placeful_wf.getWorkflowPolicyConfig(self.content.Transfers)
    placefulWfName = 'elan-transfer'
    config.setPolicyIn(policy=placefulWfName, update_security=False)
    config.setPolicyBelow(policy=placefulWfName, update_security=False)
    