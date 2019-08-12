# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.ZCatalog.ProgressHandler import ZLogHandler

def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('docpool.base_various.txt') is None:
        return
    # Add additional setup code here
    from docpool.config.general.base import install
    install(context.getSite())
    cat = getToolByName(context.getSite(), "portal_catalog")
    cat.reindexIndex(["dp_type", "mdate", "changed"], REQUEST=context.getSite().REQUEST)

