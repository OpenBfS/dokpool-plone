# -*- coding: utf-8 -*-


def setupVarious(context):

    # Ordinarily, GenericSetup handlers check for the existence of XML files.
    # Here, we are not parsing an XML file, but we use this text file as a
    # flag to check that we actually meant for this import step to be run.
    # The file is found in profiles/default.

    if context.readDataFile('docpool.rodos_various.txt') is None:
        return
    # TODO: Add additional setup code here
    from docpool.rodos.general.rodos import install

    install(context.getSite())
