# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
##code-section import
##/code-section import

def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('docpool.example_various.txt') is None:
        return
##code-section setupcode
    # TODO: Add additional setup code here
##/code-section setupcode

##code-section Main
##/code-section Main 