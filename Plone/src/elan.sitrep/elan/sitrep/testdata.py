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
from elan.policy.chomsky import chomsky
from loremipsum import get_paragraphs
from elan.esd.behaviors.elandocument import IELANDocument
from docpool.config.utils import ID, TITLE, TYPE, CHILDREN, createPloneObjects

    
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
             {TYPE: 'SRScenario', TITLE: 'Scenario 2', ID: 'scenario2', CHILDREN: PHASES}, 
             {TYPE: 'SRScenario', TITLE: 'Scenario 3', ID: 'scenario3', CHILDREN: PHASES}, 
             ]
SRCONFIG = [
            {TYPE: 'SRConfig', TITLE: 'SR Configuration', ID: 'srconfig', CHILDREN: SCENARIOS },
            {TYPE: 'SRCollections', TITLE: 'SR Collections', ID: 'colls', CHILDREN: [] },
            {TYPE: 'SRTextBlocks', TITLE: 'Text Blocks', ID: 'textblocks', CHILDREN: [] },
            ]

def createModuleTypes(self, fresh):
    """
    """
    createPloneObjects(self.config.dtypes, MODULE_TYPES, fresh)
    
def createSRConfig(self, fresh):
    """
    """
    createPloneObjects(self.config, SRCONFIG, fresh)

def createSO(self, fresh):
    """
    """
    createPloneObjects(self.esd, SITUATION_OVERVIEW, fresh)

    
def deleteTestData(context):
    """
    """
    pass
    
def createTestData(context, fresh=1):
    """
    """
    createModuleTypes(context, fresh)
    createSRConfig(context, fresh)
    createSO(context, fresh)
    return context.restrictedTraverse('@@view')()
