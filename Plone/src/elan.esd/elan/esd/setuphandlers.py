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

    if context.readDataFile('elan.esd_various.txt') is None:
        return
##code-section setupcode
    # Add additional setup code here
    cat = getToolByName(context.getSite(), "portal_catalog")
    
    extend_allowed_types(context.getSite(), 'DocumentPool', ["ELANContentConfig","ELANArchives","ELANCurrentSituation","ELANInfos"])
#    extend_behaviors(context.getSite(), 'DPDocument', ['elan.esd.behaviors.elandocument.IELANDocument'])
#    extend_behaviors(context.getSite(), 'DPDocument', ['elan.esd.behaviors.transferable.ITransferable'])
#    extend_behaviors(context.getSite(), 'DocType', ['elan.esd.behaviors.elandoctype.IELANDocType'])
    cat.reindexIndex(["scenarios", "category"], REQUEST=context.getSite().REQUEST)
#    cat.refreshCatalog(clear=False,pghandler=ZLogHandler(100))
    
##/code-section setupcode

##code-section Main
def extend_allowed_types(context, type_name, new_types):
    ttool = getToolByName(context, "portal_types")
    obj = ttool._getOb(type_name)
    allowed_types = list(obj.getProperty("allowed_content_types"))
    allowed_types.extend(new_types)
    obj._updateProperty("allowed_content_types", allowed_types)
    obj.reindexObject()
    
def extend_behaviors(context, type_name, new_behaviors):
    """
    """
    ttool = getToolByName(context, 'portal_types')
    obj = ttool._getOb(type_name)
    behaviors = list(obj.getProperty("behaviors"))
    behaviors.extend(new_behaviors)
    obj._updateProperty("behaviors", behaviors)
    obj.reindexObject()
##/code-section Main 