# -*- coding: utf-8 -*-
from utils import install
from Products.CMFCore.utils import getToolByName
from Products.ZCatalog.ProgressHandler import ZLogHandler

def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('elan.policy_various.txt') is None:
        return
    portal = context.getSite()
    install(portal)
    wtool = getToolByName(portal, 'portal_workflow')
    wtool.updateRoleMappings()    
    cat = getToolByName(context.getSite(), "portal_catalog")
#    cat.refreshCatalog(clear=True,pghandler=ZLogHandler(100))
#    This would destroy the scenarios index
    