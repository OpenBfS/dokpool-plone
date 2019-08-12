# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName


def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('elan.esd_various.txt') is None:
        return
    # Add additional setup code here
    cat = getToolByName(context.getSite(), "portal_catalog")

    extend_allowed_types(
        context.getSite(),
        'DocumentPool',
        ["ELANContentConfig", "ELANArchives", "ELANCurrentSituation", "ELANInfos"],
    )
    cat.reindexIndex(["scenarios", "category"], REQUEST=context.getSite().REQUEST)


#    cat.refreshCatalog(clear=False,pghandler=ZLogHandler(100))


def extend_allowed_types(context, type_name, new_types):
    ttool = getToolByName(context, "portal_types")
    obj = ttool._getOb(type_name)
    allowed_types = list(obj.getProperty("allowed_content_types"))
    allowed_types.extend(new_types)
    obj._updateProperty("allowed_content_types", allowed_types)
    obj.reindexObject()
