# -*- coding: utf-8 -*-

import transaction
import time
from zExceptions import BadRequest
# from Acquisition import aq_base

# from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from Products.CMFPlone.utils import safe_unicode
from plone.app.textfield.value import RichTextValue
import datetime
from Products.CMFCore.utils import getToolByName
import random

from docpool.elan.config import ELAN_APP
from elan.policy.chomsky import chomsky
from loremipsum import get_paragraphs
from elan.esd.behaviors.elandocument import IELANDocument
from docpool.config.utils import ID, TITLE, TYPE, CHILDREN, createPloneObjects
from docpool.base.utils import queryForObjects
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from z3c.relationfield.relation import RelationValue
from docpool.config.general import DOCTYPES
from elan.sitrep.vocabularies import ModuleTypesVocabularyFactory

    
SITUATION_OVERVIEW =  [{TYPE: 'SituationOverview', TITLE: 'Situation Overview', ID: 'sitview'}]
MODULE_TYPES = [
                {TYPE: 'SRModuleType', TITLE: 'Module 1', ID: 'mod1', CHILDREN: [] },                
                {TYPE: 'SRModuleType', TITLE: 'Module 2', ID: 'mod2', CHILDREN: [] },                
                {TYPE: 'SRModuleType', TITLE: 'Module 3', ID: 'mod3', CHILDREN: [] },                
                {TYPE: 'SRModuleType', TITLE: 'Module 4', ID: 'mod4', CHILDREN: [] },                
                {TYPE: 'SRModuleType', TITLE: 'Module 5', ID: 'mod5', CHILDREN: [] },                
                {TYPE: 'SRModuleType', TITLE: 'Module 6', ID: 'mod6', CHILDREN: [] },                
                {TYPE: 'SRModuleType', TITLE: 'Module 7', ID: 'mod7', CHILDREN: [] },                
                {TYPE: 'SRModuleType', TITLE: 'Module 8', ID: 'mod8', CHILDREN: [] },                
                {TYPE: 'SRModuleType', TITLE: 'Module 9', ID: 'mod9', CHILDREN: [] },                
                ]
MODULES = [ {TYPE: 'SRModuleConfig', TITLE: 'Module 1', ID: 'mod1', 'modType': 'mod1', CHILDREN: [] },
            {TYPE: 'SRModuleConfig', TITLE: 'Module 2', ID: 'mod2', 'modType': 'mod2', CHILDREN: [] },
            {TYPE: 'SRModuleConfig', TITLE: 'Module 3', ID: 'mod3', 'modType': 'mod3', CHILDREN: [] },
            {TYPE: 'SRModuleConfig', TITLE: 'Module 4', ID: 'mod4', 'modType': 'mod4', CHILDREN: [] },
            {TYPE: 'SRModuleConfig', TITLE: 'Module 5', ID: 'mod5', 'modType': 'mod5', CHILDREN: [] },
            {TYPE: 'SRModuleConfig', TITLE: 'Module 6', ID: 'mod6', 'modType': 'mod6', CHILDREN: [] },
            {TYPE: 'SRModuleConfig', TITLE: 'Module 7', ID: 'mod7', 'modType': 'mod7', CHILDREN: [] },
            {TYPE: 'SRModuleConfig', TITLE: 'Module 8', ID: 'mod8', 'modType': 'mod8', CHILDREN: [] },
            {TYPE: 'SRModuleConfig', TITLE: 'Module 9', ID: 'mod9', 'modType': 'mod9', CHILDREN: [] },
           ]
PHASES = [ 
          {TYPE: 'SRPhase', TITLE: 'Phase 1', ID: 'phase1', CHILDREN: MODULES}, 
          {TYPE: 'SRPhase', TITLE: 'Phase 2', ID: 'phase2', CHILDREN: MODULES}, 
          {TYPE: 'SRPhase', TITLE: 'Phase 3', ID: 'phase3', CHILDREN: MODULES}, 
          {TYPE: 'SRPhase', TITLE: 'Phase 4', ID: 'phase4', CHILDREN: MODULES}, 
          ]
SCENARIOS = [
             {TYPE: 'SRScenario', TITLE: 'Scenario 1', ID: 'scenario1', CHILDREN: PHASES}, 
#             {TYPE: 'SRScenario', TITLE: 'Scenario 2', ID: 'scenario2', CHILDREN: PHASES}, 
#             {TYPE: 'SRScenario', TITLE: 'Scenario 3', ID: 'scenario3', CHILDREN: PHASES}, 
             ]

MODTYPES = [
            {TYPE: 'SRModuleTypes', TITLE: 'SR Module Types', ID: 'mtypes', CHILDREN: MODULE_TYPES },            
            ]
SRCONFIG = [
            {TYPE: 'SRConfig', TITLE: 'SR Configuration', ID: 'srconfig', CHILDREN: SCENARIOS },
            {TYPE: 'SRCollections', TITLE: 'SR Collections', ID: 'colls', CHILDREN: [
                                                                                    
                {TYPE: 'SRCollection', TITLE: u'CNCAN PROJECTIONS', ID: 'cncan-projections', CHILDREN: [], DOCTYPES: ['cncanprojection']},
                {TYPE: 'SRCollection', TITLE: u'IFIN PROJECTIONS', ID: 'ifin-projections', CHILDREN: [], DOCTYPES: ['ifinprojection']},
                {TYPE: 'SRCollection', TITLE: u'NPP PROJECTIONS', ID: 'npp-projections', CHILDREN: [], DOCTYPES: ['nppprojection']},
                                                                                     ] },
            {TYPE: 'SRTextBlocks', TITLE: 'Text Blocks', ID: 'textblocks', CHILDREN: [] },
            ]

def createModuleTypes(self, fresh):
    """
    """
    createPloneObjects(self.config, MODTYPES, fresh)
    
def createSRConfig(self, fresh):
    """
    """
    createPloneObjects(self.contentconfig, SRCONFIG, fresh)

def createSO(self, fresh):
    """
    """
    createPloneObjects(self.esd, SITUATION_OVERVIEW, fresh)

    
def createTextBlocks(self, count=20):
    """
    """
    path = self.contentconfig.srconfig.textblocks
    for i in range(0, count):
        # random user
        docid = "tb_%d" % i
        # Generate random text for description
        
        d = chomsky(2)
        t = "<p>" + "</p><p>".join(get_paragraphs(3)) + "</p>"

        if not hasattr(path, docid):        
            path.invokeFactory(id=docid, type_name="SRTextBlock", title="Textblock %d" % i, description="")
            d = path._getOb(docid)
            d.text = RichTextValue(safe_unicode(t))
            d.reindexObject()
            
def referenceTextBlocksAndCollections(self):
    """
    """
    path = self.dpSearchPath() + "/contentconfig"
    mconfigs = [ mc.getObject() for mc in queryForObjects(self, path = path, portal_type='SRModuleConfig') ] 
    tbs = [ tb.getObject() for tb in queryForObjects(self, path = path, portal_type='SRTextBlock') ]
    colls = [ coll.getObject() for coll in queryForObjects(self, path = path, portal_type='SRCollection') ]
    intids = getUtility(IIntIds)
    for mconfig in mconfigs:
        refs = []
        for i in range(0,5):
            idx = int(round(random.random() * 19.0))
            #print idx
            to_id = intids.getId(tbs[idx])
            refs.append(RelationValue(to_id))
        mconfig.textBlocks = refs
        idx = int(round(random.random() * 2.0))
        to_id = intids.getId(colls[idx])
        mconfig.docSelection = RelationValue(to_id)
        
def createSituationReport(self):
    """
    """
    prefix = self.prefix or self.getId()
    gname = "%s_Group%d" % (prefix, 2)
    g = None
    try:
        g = self.content.Groups[gname]
    except:
        return
    createPloneObjects(g, [ {TYPE: 'SRFolder', TITLE: 'Lagebericht', ID: 'lagebericht', CHILDREN: [] } ])
    path = g.lagebericht
    intids = getUtility(IIntIds)

    for mt in ModuleTypesVocabularyFactory(self, raw=True):
        
        docid = mt[0]
        # Generate random text for description
        
        d = chomsky(2)
        t = "<p>" + "</p><p>".join(get_paragraphs(3)) + "</p>"

        if not hasattr(path, docid):        
            path.invokeFactory(id=docid, type_name="SRModule", title=mt[1], description="")
            d = path._getOb(docid)
            d.text = RichTextValue(safe_unicode(t))
            d.docType = mt[0]
            d.extension(ELAN_APP).scenarios = ["scenario1", "scenario2"]
            d.reindexObject()
            d.publishModule(justDoIt=True)
    
    transaction.commit()
    if not hasattr(path, "lage"):        
        path.invokeFactory(id="lage", type_name="SituationReport", title="Aktueller Lagebericht", description="")
        d = path._getOb("lage")
        t = "<p>" + "</p><p>".join(get_paragraphs(3)) + "</p>"
        d.text = RichTextValue(safe_unicode(t))
        phase = self.contentconfig.srconfig.scenario1.phase1
        to_id = intids.getId(phase)
        d.phase = RelationValue(to_id)
        mods = [ m.getObject() for m in queryForObjects(self, path = "/".join(path.getPhysicalPath()), portal_type='SRModule', review_state='published', sort_on='getId') ] 
        refs = []
        for mod in mods:
            #print idx
            to_id = intids.getId(mod)
            refs.append(RelationValue(to_id))
        d.currentModules=refs
        d.extension(ELAN_APP).scenarios = ["scenario1", "scenario2"]
        d.reindexObject()
        d.publishReport(justDoIt=True, duplicate=True)
    
    
def deleteTestData(context):
    """
    """
    pass
    
def createTestData(context, fresh=1):
    """
    """
    createModuleTypes(context, fresh)
    createSRConfig(context, fresh)
    createTextBlocks(context, count=20)
    transaction.commit()
    referenceTextBlocksAndCollections(context)
    createSituationReport(context)
    return context.restrictedTraverse('@@view')()
