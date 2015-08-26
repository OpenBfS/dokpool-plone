# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.PortalTransforms.Transform import make_config_persistent
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
import transaction
from Products.PythonScripts.PythonScript import PythonScript
from docpool.base.events import IDocumentPoolUndeleteable
from Products.Five.utilities.marker import mark
from Products.CMFPlone.interfaces.constrains import ISelectableConstrainTypes
from plone.app.dexterity.behaviors import constrains
from docpool.config.utils import ID, TYPE, TITLE, CHILDREN, createPloneObjects
from docpool.config import _
from plone.app.textfield.value import RichTextValue

DOCTYPES='ref_setDocTypesUpdateCollection' # indicates that docTypes is referencing objects, which need to be queried by their id


# Structure definitions
# CHANGE HERE. DocTypes, DocCollections and their connections must match.

DTYPES = [{TYPE: 'DocType', TITLE: u'Event Information', ID: 'eventinformation'},
          {TYPE: 'DocType', TITLE: u'Notification', ID: 'notification'},
          {TYPE: 'DocType', TITLE: u'NPP Information', ID: 'nppinformation'},
          {TYPE: 'DocType', TITLE: u'Weather Information', ID: 'weatherinformation'},
          {TYPE: 'DocType', TITLE: u'Trajectory', ID: 'trajectory'},
          {TYPE: 'DocType', TITLE: u'CNCAN Projection', ID: 'cncanprojection'},
          {TYPE: 'DocType', TITLE: u'IFIN Projection', ID: 'ifinprojection'},
          {TYPE: 'DocType', TITLE: u'NPP Projection', ID: 'nppprojection'},
          {TYPE: 'DocType', TITLE: u'RODOS Projection', ID: 'rodosprojection'},
          {TYPE: 'DocType', TITLE: u'Other Projection', ID: 'otherprojection'},
          {TYPE: 'DocType', TITLE: u'Gamma Dose Rate', ID: 'gammadoserate'},
          {TYPE: 'DocType', TITLE: u'Air Activity', ID: 'airactivity'},
          {TYPE: 'DocType', TITLE: u'Ground Contamination', ID: 'groundcontamination'},
          {TYPE: 'DocType', TITLE: u'Measurement Result Feed', ID: 'mresult_feed'},
          {TYPE: 'DocType', TITLE: u'Measurement Result Food', ID: 'mresult_food'},
          {TYPE: 'DocType', TITLE: u'Measurement Result Water', ID: 'mresult_water'},
          {TYPE: 'DocType', TITLE: u'Situation Report', ID: 'situationreport'},
          {TYPE: 'DocType', TITLE: u'Instructions to the Public', ID: 'instructions'},
          {TYPE: 'DocType', TITLE: u'Protective Actions', ID: 'protectiveactions'},
          {TYPE: 'DocType', TITLE: u'Media Release', ID: 'mediarelease'}
          ]

ESDCOLLECTIONS = [{TYPE: 'ELANSection', TITLE: u'INCIDENT', ID: 'incident', CHILDREN: [
                                                                            {TYPE: 'ELANDocCollection', TITLE: u'NOTIFICATIONS', ID: 'notifications', CHILDREN: [], DOCTYPES: ['notification']},
                                                                            {TYPE: 'ELANDocCollection', TITLE: u'EVENT / NPP INFORMATION', ID: 'event-npp-information', CHILDREN: [],DOCTYPES: ['eventinformation','nppinformation']},
                                                                            ]},
                  {TYPE: 'ELANSection', TITLE: u'METEOROLOGY', ID: 'meteorology', CHILDREN: [
                                                                            {TYPE: 'ELANDocCollection', TITLE: u'WEATHER INFORMATION', ID: 'weather-information', CHILDREN: [], DOCTYPES: ['weatherinformation']},
                                                                            {TYPE: 'ELANDocCollection', TITLE: u'TRAJECTORIES', ID: 'trajectories', CHILDREN: [], DOCTYPES: ['trajectory']},
                                                                            ]},
                  {TYPE: 'ELANSection', TITLE: u'DOSE PROJECTIONS', ID: 'dose-projections', CHILDREN: [
                                                                            {TYPE: 'ELANDocCollection', TITLE: u'CNCAN PROJECTIONS', ID: 'cncan-projections', CHILDREN: [], DOCTYPES: ['cncanprojection']},
                                                                            {TYPE: 'ELANDocCollection', TITLE: u'IFIN PROJECTIONS', ID: 'ifin-projections', CHILDREN: [], DOCTYPES: ['ifinprojection']},
                                                                            {TYPE: 'ELANDocCollection', TITLE: u'NPP PROJECTIONS', ID: 'npp-projections', CHILDREN: [], DOCTYPES: ['nppprojection']},
                                                                            {TYPE: 'ELANDocCollection', TITLE: u'RODOS', ID: 'rodos', CHILDREN: [], DOCTYPES: ['rodosprojection']},
                                                                            {TYPE: 'ELANDocCollection', TITLE: u'OTHER', ID: 'other', CHILDREN: [], DOCTYPES: ['otherprojection']},
                                                                            ]},
                  {TYPE: 'ELANSection', TITLE: u'MEASUREMENT RESULTS', ID: 'measurement-results', CHILDREN: [
                                                                            {TYPE: 'ELANDocCollection', TITLE: u'GAMMA DOSE RATE', ID: 'gamma-dose-rate', CHILDREN: [], DOCTYPES: ['gammadoserate']},
                                                                            {TYPE: 'ELANDocCollection', TITLE: u'AIR ACTIVITY', ID: 'air-activity', CHILDREN: [], DOCTYPES: ['airactivity']},
                                                                            {TYPE: 'ELANDocCollection', TITLE: u'GROUND CONTAMINATION', ID: 'ground-contamination', CHILDREN: [], DOCTYPES: ['groundcontamination']},
                                                                            {TYPE: 'ELANDocCollection', TITLE: u'FOOD AND FEED', ID: 'food-and-feed', CHILDREN: [], DOCTYPES: ['mresult_feed', 'mresult_food']},
                                                                            {TYPE: 'ELANDocCollection', TITLE: u'WATER', ID: 'water', CHILDREN: [], DOCTYPES: ['mresult_water']},
                                                                            ]},
                  {TYPE: 'ELANSection', TITLE: u'CURRENT SITUATION', ID: 'current-situation', CHILDREN: [
                                                                            {TYPE: 'ELANDocCollection', TITLE: u'SITUATION REPORTS', ID: 'situation-reports', CHILDREN: [], DOCTYPES: ['nppinformation', 'situationreport']},
                                                                            {TYPE: 'ELANDocCollection', TITLE: u'PROTECTIVE ACTIONS', ID: 'protective-actions', CHILDREN: [], DOCTYPES: ['instructions','protectiveactions']},
                                                                            ]},
                  {TYPE: 'ELANSection', TITLE: u'INFORMATION OF THE PUBLIC', ID: 'information-of-the-public', CHILDREN: [
                                                                            {TYPE: 'ELANDocCollection', TITLE: u'MEDIA RELEASES', ID: 'media-releases', CHILDREN: [],DOCTYPES: ['mediarelease']},
                                                                            {TYPE: 'ELANDocCollection', TITLE: u'INSTRUCTIONS TO THE PUBLIC', ID: 'instructions-to-the-public', CHILDREN: [], DOCTYPES: ['instructions']},
                                                                            ]},  
                  {TYPE: 'ELANDocCollection', TITLE: 'Overview', ID: 'overview', "setExcludeFromNav": True, DOCTYPES: [], CHILDREN: [] },            
                  {TYPE: 'ELANDocCollection', TITLE: 'All documents', ID: 'recent', DOCTYPES: [], CHILDREN: [] },            
              ]
       
def connectTypesAndCategories(self):
    """
    """
    from elan.esd.behaviors.elandoctype import IELANDocType
    try:
        IELANDocType(self.config.eventinformation).setCCategory('event-npp-information')
    except:
        pass
    try:
        IELANDocType(self.config.weatherinformation).setCCategory('weather-information')
    except:
        pass
    try:
        IELANDocType(self.config.trajectory).setCCategory('trajectories')
    except:
        pass
    try:
        IELANDocType(self.config.cncanprojection).setCCategory('cncan-projections')
    except:
        pass
    try:
        IELANDocType(self.config.ifinprojection).setCCategory('ifin-projections')
    except:
        pass
    try:
        IELANDocType(self.config.nppprojection).setCCategory('npp-projections')
    except:
        pass
    try:
        IELANDocType(self.config.rodosprojection).setCCategory('rodos')
    except:
        pass
    try:
        IELANDocType(self.config.otherprojection).setCCategory('other')
    except:
        pass
    try:
        IELANDocType(self.config.gammadoserate).setCCategory('gamma-dose-rate')
    except:
        pass
    try:
        IELANDocType(self.config.airactivity).setCCategory('air-activity')
    except:
        pass
    try:
        IELANDocType(self.config.groundcontamination).setCCategory('ground-contamination')
    except:
        pass
    try:
        IELANDocType(self.config.mresult_feed).setCCategory('food-and-feed')
    except:
        pass
    try:
        IELANDocType(self.config.mresult_food).setCCategory('food-and-feed')
    except:
        pass
    try:
        IELANDocType(self.config.mresult_water).setCCategory('water')
    except:
        pass
    try:
        IELANDocType(self.config.situationreport).setCCategory('situation-reports')
    except:
        pass
    try:
        IELANDocType(self.config.protectiveactions).setCCategory('protective-actions')
    except:
        pass
    try:
        IELANDocType(self.config.mediarelease).setCCategory('media-releases')
    except:
        pass
    try:
        IELANDocType(self.config.instructions).setCCategory('instructions-to-the-public')
    except:
        pass
    try:
        IELANDocType(self.config.notification).setCCategory('notifications')
    except:
        pass
    try:
        IELANDocType(self.config.nppinformation).setCCategory('event-npp-information')
    except:
        pass


# Further base structures

FRONTPAGE = RichTextValue(u"", 'text/plain', 'text/html')

                       
BASICSTRUCTURE = [{TYPE: 'ELANCurrentSituation', TITLE: 'Current Situation Template', ID: 'esd', CHILDREN: [ 
                         {TYPE: 'Document', TITLE: u'Electronic Situation Display', ID: 'front-page', 'text': FRONTPAGE, CHILDREN: [] }                                                                        
                                                                                                 ]},
                  ]

ADMINSTRUCTURE = [
                  {TYPE: 'DocTypes', TITLE: u'Global Document Types', ID: 'config', CHILDREN: DTYPES},                                                         
                  {TYPE: 'ELANContentConfig', TITLE: 'Content Configuration', ID: 'contentconfig', CHILDREN: [
                        {TYPE: 'Text', TITLE: u'Impressum', ID: 'impressum', CHILDREN: []},
                        {TYPE: 'Text', TITLE: u'Help', ID: 'help', CHILDREN: []},
                        ]}
                 ]

BASICSTRUCTURE2 = [{TYPE: 'ELANCurrentSituation', TITLE: 'Current Situation Template', ID: 'esd', CHILDREN: ESDCOLLECTIONS},
                  ]



# Configuration methods

def configUserFolders(self, fresh):
    """
    """
    # Turn creation of user folders on
#    from plone.app.controlpanel.security import ISecuritySchema
    # Fetch the adapter
    from Products.CMFPlone.interfaces.controlpanel import ISecuritySchema
    security_adapter =  ISecuritySchema(self)
    security_adapter.set_enable_user_folders(True)
    
    # Set type for user folders
    mtool = getToolByName(self,"portal_membership")
    mtool.setMemberAreaType("UserFolder")
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
    
def navSettings(self):    
    IExcludeFromNavigation(self.news).exclude_from_nav = True
    self.news.reindexObject()
    IExcludeFromNavigation(self.events).exclude_from_nav = True
    self.events.reindexObject()
    IExcludeFromNavigation(self.Members).exclude_from_nav = True
    self.Members.reindexObject() 
    
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
    createPloneObjects(plonesite, ADMINSTRUCTURE, fresh)

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
    #mark(plonesite.contentconfig.ticker, IELANUndeleteable)
    # Correct addable types now that the structures has been created.
    # We only allow more Sections in the esd node.
    #print plonesite.esd
    
    BASETYPES = ['ELANSection']
    esdBehavior = ISelectableConstrainTypes(plonesite.esd)
    esdBehavior.setConstrainTypesMode(constrains.ENABLED)
    esdBehavior.setLocallyAllowedTypes(BASETYPES)
    esdBehavior.setImmediatelyAddableTypes(BASETYPES)
    
#     plonesite.esd.setConstrainTypesMode(1) # manually constrained
#     plonesite.esd.setLocallyAllowedTypes(['ELANSection'])
#     plonesite.esd.setImmediatelyAddableTypes(['ELANSection'])
def setFrontpage(self):
    """
    """
    ttool = getToolByName(self, "portal_types")
    obj = ttool._getOb("Plone Site")
#    obj._updateProperty("default_view", "redirect")
#    obj._updateProperty("immediate_view", "redirect")
    obj.reindexObject()
    r = "redirect"
    try:
        id = self._setObject(r, PythonScript(r))
    except:
        pass
    ps = self._getOb(r)
    ps.write("""
if not context.isAdmin():
    container.REQUEST.RESPONSE.redirect(context.myFirstDocumentPool())
else:
    container.REQUEST.RESPONSE.redirect(context.absolute_url() + "/folder_contents")
""")
    self.setDefaultPage(r)
    
    self.esd.setDefaultPage("front-page")
    

def configureFiltering(self):
    """
    """    
    tid = 'safe_html'

    pt = getToolByName(self, 'portal_transforms')
    if not tid in pt.objectIds(): return

    trans = pt[tid]

    tconfig = trans._config
    tconfig['class_blacklist'] = []
    tconfig['nasty_tags'] = {'meta': '1'}
    tconfig['remove_javascript'] = 0
    tconfig['stripped_attributes'] = ['lang', 'valign', 'halign', 'border',
                                     'frame', 'rules', 'cellspacing',
                                     'cellpadding', 'bgcolor']
    tconfig['stripped_combinations'] = {}
    tconfig['style_whitelist'] = ['text-align', 'list-style-type', 'float',
                                  'width', 'height', 'padding-left',
                                  'padding-right'] # allow specific styles for
    tconfig['valid_tags'] = {
        'code': '1', 'meter': '1', 'tbody': '1', 'style': '1', 'img': '0',
        'title': '1', 'tt': '1', 'tr': '1', 'param': '1', 'li': '1',
        'source': '1', 'tfoot': '1', 'th': '1', 'td': '1', 'dl': '1',
        'blockquote': '1', 'big': '1', 'dd': '1', 'kbd': '1', 'dt': '1',
        'p': '1', 'small': '1', 'output': '1', 'div': '1', 'em': '1',
        'datalist': '1', 'hgroup': '1', 'video': '1', 'rt': '1', 'canvas': '1',
        'rp': '1', 'sub': '1', 'bdo': '1', 'sup': '1', 'progress': '1',
        'body': '1', 'acronym': '1', 'base': '0', 'br': '0', 'address': '1',
        'article': '1', 'strong': '1', 'ol': '1', 'script': '1', 'caption': '1',
        'dialog': '1', 'col': '1', 'h2': '1', 'h3': '1', 'h1': '1', 'h6': '1',
        'h4': '1', 'h5': '1', 'header': '1', 'table': '1', 'span': '1',
        'area': '0', 'mark': '1', 'dfn': '1', 'var': '1', 'cite': '1',
        'thead': '1', 'head': '1', 'hr': '0', 'link': '1', 'ruby': '1',
        'b': '1', 'colgroup': '1', 'keygen': '1', 'ul': '1', 'del': '1',
        'iframe': '1', 'embed': '1', 'pre': '1', 'figure': '1', 'ins': '1',
        'aside': '1', 'html': '1', 'nav': '1', 'details': '1', 'u': '1',
        'samp': '1', 'map': '1', 'object': '1', 'a': '1', 'footer': '1',
        'i': '1', 'q': '1', 'command': '1', 'time': '1', 'audio': '1',
        'section': '1', 'abbr': '1', 'strike': '1'}
    make_config_persistent(tconfig)
    trans._p_changed = True
    trans.reload()
    

    
def createGroups(self):
    
    gdata = getToolByName(self, 'portal_groupdata')
    try:
        gdata.manage_addProperty("allowedDocTypes", "possibleDocTypes", "multiple selection")
    except:
        pass    
    try:
        gdata.manage_addProperty("dp", "possibleDocumentPools", "selection")
    except:
        pass    
    
  