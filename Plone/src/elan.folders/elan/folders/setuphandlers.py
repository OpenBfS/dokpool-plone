# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
##code-section import
##/code-section import

def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('elan.folders_various.txt') is None:
        return
##code-section setupcode
    # Add additional setup code here
    portal = context.getSite()
    extend_allowed_types(portal, "ELANFolder")
    extend_allowed_types(portal, "ELANUserFolder")
    extend_allowed_types(portal, "ELANGroupFolder")
    
    
def extend_allowed_types(context, type_name):
    ttool = getToolByName(context, "portal_types")
    obj = ttool._getOb(type_name)
    allowed_types = list(obj.getProperty("allowed_content_types"))
    allowed_types.append("ELANCollaborationFolder")
    allowed_types.append("ELANPrivateFolder")
    allowed_types.append("ELANReviewFolder")
    obj._updateProperty("allowed_content_types", allowed_types)
    obj.reindexObject()

##/code-section setupcode

##code-section Main
##/code-section Main 