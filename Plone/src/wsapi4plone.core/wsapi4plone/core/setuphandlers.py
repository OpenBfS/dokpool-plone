from Products.CMFCore.utils import getToolByName

def importDefaults(context):
    """Run the init profile if the configuration has not been initialized."""
    if context.readDataFile('wsapi4plone.core_various.txt') is None:
        return
    portal = context.getSite()

    portal_properties = getToolByName(portal, 'portal_properties')
    properties = getToolByName(portal_properties, 'wsapi4plone_properties',
                               None)
    if properties is None:
        portal_setup = getToolByName(portal, 'portal_setup')
        portal_setup.runAllImportStepsFromProfile('profile-wsapi4plone.core:init')
