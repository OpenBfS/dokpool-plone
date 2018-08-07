# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from docpool.doksys import DocpoolMessageFactory as _

def dpAdded(self):
    """
    @param self: 
    @return: 
        
    """
    createDoksysUsers(self)
    createDoksysGroups(self)
    setDoksysLocalRoles(self)
    copyDoksysNavigation(self)
    self.reindexAll()
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
        # Group for Doksys application rights
        props = {'allowedDocTypes': [], 'title': 'Doksys Users (%s)' % title,
                 'description': 'Users with access to Doksys functions.',
                 'dp': self.UID()}
        gtool.addGroup("%s_DoksysUsers" % prefix,
                       properties=props)
        gtool.addPrincipalToGroup('%s_doksysadmin' % prefix, '%s_DoksysUsers' % prefix)
        gtool.addPrincipalToGroup('%s_doksysadmin' % prefix, '%s_Administrators' % prefix)

        # Set Doksys role as a local role for the new group
        self.manage_setLocalRoles("%s_DoksysUsers" % prefix, ["DoksysUser"])


def createDoksysUsers(self):
    # Set type for user folders
    mtool = getToolByName(self, "portal_membership")
    prefix = self.prefix or self.getId()
    prefix = str(prefix)
    title = self.Title()
    mtool.addMember('%s_doksysadmin' % prefix, 'DokSys Administrator (%s)' % title, ['Member'], [])
    doksysadmin = mtool.getMemberById('%s_doksysadmin' % prefix)
    doksysadmin.setMemberProperties(
        {"fullname": 'DokSys Administrator (%s)' % title,
         "dp": self.UID()})
    doksysadmin.setSecurityProfile(password="admin")


def setDoksysLocalRoles(self):
    """
    Normal local members: Reader
    Administrators: Site Administrator
    ContentAdministrators: Reviewer
    Receivers: Owner, Editor
    Senders: Contributor
    """
    prefix = self.prefix or self.getId()
    prefix = str(prefix)

    self.manage_setLocalRoles("%s_DokSysUsers" % prefix, ["DoksysUser"])

def copyDoksysNavigation(self):
    """

    @param self:
    @param fresh:
    @return:
    """
#    if not fresh:
#       return
    search = self.search
    from docpool.base.utils import _copyPaste
    _copyPaste(search, self, safe=False)
    self.search.setTitle(_("Standardsuchen"))
    self.search.reindexObject()
    # make sure the run display is first
    # TODO if more complex (e.g. second after 'esd')
    self.moveObject("search", 0)

