# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName

def dpAdded(self):
    """
    @param self: 
    @return: 
        
    """
    createRodosGroups(self)
    # TODO:

def dpRemoved(self):
    """
    @param self:
    @return:
    """
    # TODO:
    return

def createRodosGroups(self):
    """
    Create Group for rodos application access
    @param self: 
    @return: 
    """

    prefix = self.prefix or self.getId()
    prefix = str(prefix)
    title = self.Title()
    gtool = getToolByName(self, 'portal_groups')
    # Group for Rodos application rights
    props = {'allowedDocTypes': [], 'title': 'Rodos Users (%s)' % title,
             'description': 'Users with access to Rodos functions.',
             'dp': self.UID()}
    gtool.addGroup("%s_RodosUsers" % prefix,
               properties=props)
    gtool.addPrincipalToGroup('%s_dpadmin' % prefix, '%s_RodosUsers' % prefix)

    # Set Rodos role as a local role for the new group
    self.manage_setLocalRoles("%s_RodosUsers" % prefix, ["RodoseUser"])

