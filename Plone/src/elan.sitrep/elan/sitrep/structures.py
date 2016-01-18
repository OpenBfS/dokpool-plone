# -*- coding: utf-8 -*-
from docpool.config.utils import ID, TITLE, TYPE, CHILDREN, createPloneObjects
from docpool.config.general import DOCTYPES


SITUATION_OVERVIEW =  [{TYPE: 'SituationOverview', TITLE: 'Situation Overview', ID: 'sitview'}]

MODTYPES = [
            {TYPE: 'SRModuleTypes', TITLE: 'SR Module Types', ID: 'mtypes', CHILDREN: [] },            
            ]
SRCONFIG = [
            {TYPE: 'SRConfig', TITLE: 'SR Configuration', ID: 'srconfig', CHILDREN: [] },
            {TYPE: 'SRCollections', TITLE: 'SR Collections', ID: 'colls', CHILDREN: [
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

def createConfig(obj, fresh=1):
    """
    """
    self = obj
    createModuleTypes(self, fresh)
    createSRConfig(self, fresh)
    createSO(self, fresh)
    
