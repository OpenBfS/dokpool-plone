# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName

def dpAdded(self):
    """
    @param self: 
    @return: 
        
    """
    createRODOSGroups(self)
    # TODO:

def dpRemoved(self):
    """
    @param self:
    @return:
    """
    # TODO:
    return

def createRODOSGroups(self):
    """
    Create Group for rodos application access
    @param self: 
    @return: 
    """

    prefix = self.prefix or self.getId()
    prefix = str(prefix)
    title = self.Title()
    gtool = getToolByName(self, 'portal_groups')
    # Group for RODOS application rights
    props = {'allowedDocTypes': [], 'title': 'RODOS Users (%s)' % title,
             'description': 'Users with access to RODOS functions.',
             'dp': self.UID()}
    gtool.addGroup("%s_RODOSUsers" % prefix,
               properties=props)
    gtool.addPrincipalToGroup('%s_dpadmin' % prefix, '%s_RODOSUsers' % prefix)

    # Set RODOS role as a local role for the new group
    self.manage_setLocalRoles("%s_RODOSUsers" % prefix, ["RODOSeUser"])

