# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName

def dpAdded(self):
    """
    @param self: 
    @return: 
        
    """
    createDoksysGroups(self)
    # TODO:

def dpRemoved(self):
    """
    @param self:
    @return:
    """
    # TODO:
    return

def createDoksysGroups(self):
        """
        Create Group for doksys application access
        @param self:
        @return:
        """

        prefix = self.prefix or self.getId()
        prefix = str(prefix)
        title = self.Title()
        gtool = getToolByName(self, 'portal_groups')
        # Group for Example application rights
        props = {'allowedDocTypes': [], 'title': 'Doksys Users (%s)' % title,
                 'description': 'Users with access to Doksys functions.',
                 'dp': self.UID()}
        gtool.addGroup("%s_DoksysUsers" % prefix,
                       properties=props)
        gtool.addPrincipalToGroup('%s_dpadmin' % prefix, '%s_DoksysUsers' % prefix)

        # Set Example role as a local role for the new group
        self.manage_setLocalRoles("%s_DoksysUsers" % prefix, ["DoksysUser"])
