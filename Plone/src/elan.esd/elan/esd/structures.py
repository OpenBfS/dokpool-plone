# -*- coding: utf-8 -*-
from docpool.base.content.documentpool import IDocumentPool, DocumentPool
from docpool.base.content import documentpool
from zope.component import adapter
from zope.lifecycleevent import IObjectAddedEvent, IObjectRemovedEvent
import transaction
from elan.policy.utils import createPloneObjects, CHILDREN, ID, TITLE, TYPE
from Products.Archetypes.utils import shasattr
from Products.CMFCore.utils import getToolByName
from zExceptions import BadRequest
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from Products.CMFPlone.utils import log, log_exc
from elan.esd import ELAN_EMessageFactory as _

specialAttributes=(TYPE, TITLE, ID, CHILDREN)

TRANSFER_AREA = [
                    {TYPE: 'ELANTransfers', TITLE: u'Transfers', ID: 'Transfers', CHILDREN: []},                                                                                                                                                                                            
               ]
                            
BASICSTRUCTURE = [
                  {TYPE: 'ELANArchives', TITLE: u'Archive', ID: 'archive', CHILDREN: []},
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



PLONE_UTILS=None


# @adapter(IDocumentPool, IObjectAddedEvent)
def esdAdded(obj, event=None):
    """
    """
    self = obj
    createStructure(self, True)
    createContentArea(self, True)
    connectTypesAndCategories(self)
    createUsers(self)
    createGroups(self)
    setLocalRoles(self)
    self.reindexAll()
# documentpool.esdAdded = esdAdded


def createStructure(self, fresh):
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

def createContentArea(self, fresh):
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

def connectTypesAndCategories(self):
    """
    Those standard types are not necessarily there.
    """
    try:
        self.config.eventinformation.setCCategory('event-npp-information')
    except:
        pass
    try:
        self.config.weatherinformation.setCCategory('weather-information')
    except:
        pass
    try:
        self.config.trajectory.setCCategory('trajectories')
    except:
        pass
    try:
        self.config.cncanprojection.setCCategory('cncan-projections')
    except:
        pass
    try:
        self.config.ifinprojection.setCCategory('ifin-projections')
    except:
        pass
    try:
        self.config.nppprojection.setCCategory('npp-projections')
    except:
        pass
    try:
        self.config.rodosprojection.setCCategory('rodos')
    except:
        pass
    try:
        self.config.otherprojection.setCCategory('other')
    except:
        pass
    try:
        self.config.gammadoserate.setCCategory('gamma-dose-rate')
    except:
        pass
    try:
        self.config.airactivity.setCCategory('air-activity')
    except:
        pass
    try:
        self.config.groundcontamination.setCCategory('ground-contamination')
    except:
        pass
    try:
        self.config.mresult_feed.setCCategory('food-and-feed')
    except:
        pass
    try:
        self.config.mresult_food.setCCategory('food-and-feed')
    except:
        pass
    try:
        self.config.mresult_water.setCCategory('water')
    except:
        pass
    try:
        self.config.situationreport.setCCategory('situation-reports')
    except:
        pass
    try:
        self.config.protectiveactions.setCCategory('protective-actions')
    except:
        pass
    try:
        self.config.mediarelease.setCCategory('media-releases')
    except:
        pass
    try:
        self.config.instructions.setCCategory('instructions-to-the-public')
    except:
        pass
    try:
        self.config.notification.setCCategory('notifications')
    except:
        pass
    try:
        self.config.nppinformation.setCCategory('event-npp-information')
    except:
        pass
    
def deleteGroups(self):
    """
    """
    prefix = (hasattr(self, 'prefix') and self.prefix) or self.getId()
    prefix = str(prefix)
    gtool = getToolByName(self, 'portal_groups')
    # list existing groups and then delete them
    gids = gtool.getGroupIds()
    for gid in gids:
        if gid.startswith(prefix):
            gtool.removeGroup(gid) # also deletes the group folder via event subscribers

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

def createUsers(self):    
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

def deleteUsers(self):
    """
    """
    prefix = (hasattr(self, 'prefix') and self.prefix) or self.getId()
    prefix = str(prefix)
    mtool = getToolByName(self, 'portal_membership', None)
    # list all users for this ESD and delete them
    uids = mtool.listMemberIds()
    for uid in uids:
        if uid.startswith(prefix):
            try:
                mtool.deleteMembers([uid]) # also deletes the member folders
            except Exception, e:
                log_exc(e)

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
    self.contentconfig.manage_setLocalRoles("%s_ContentAdministrators" % prefix, ["Reviewer"])
    self.content.Transfers.manage_setLocalRoles("%s_Receivers" % prefix, ["Owner"])
    self.esd.manage_setLocalRoles("%s_Receivers" % prefix, ["Reviewer"])
    self.content.Transfers.manage_setLocalRoles("%s_Administrators" % prefix, ["Owner"])
    self.contentconfig.scen.manage_setLocalRoles("%s_Receivers" % prefix, ["Editor"])
    self.config.manage_setLocalRoles("%s_Receivers" % prefix, ["Editor"])
    self.content.Groups.manage_setLocalRoles("%s_Senders" % prefix, ["Contributor"])

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

