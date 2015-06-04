# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
##code-section import
from Products.ZCatalog.ProgressHandler import ZLogHandler
##/code-section import

def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('docpool.base_various.txt') is None:
        return
##code-section setupcode
    # Add additional setup code here
    cat = getToolByName(context.getSite(), "portal_catalog")
    cat.reindexIndex(["dp_type", "mdate", "changed"], REQUEST=context.getSite().REQUEST)
#    cat.refreshCatalog(clear=False,pghandler=ZLogHandler(100))
    
    portal = context.getSite()
    extend_allowed_types(portal, "SimpleFolder")
    extend_allowed_types(portal, "UserFolder")
    extend_allowed_types(portal, "GroupFolder")
    
    
def extend_allowed_types(context, type_name):
    ttool = getToolByName(context, "portal_types")
    obj = ttool._getOb(type_name)
    allowed_types = list(obj.getProperty("allowed_content_types"))
    allowed_types.append("CollaborationFolder")
    allowed_types.append("PrivateFolder")
    allowed_types.append("ReviewFolder")
    obj._updateProperty("allowed_content_types", allowed_types)
    obj.reindexObject()
    
    
##/code-section setupcode

##code-section Main
##/code-section Main 