# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
import transaction
from docpool.rei import DocpoolMessageFactory as _




def dpAdded(self):
    """
    @param self: 
    @return: 
        
    """
    fresh = True
    if self.hasObject("rei"):
        fresh = False # It's a reinstall

    copyRunDisplay(self, fresh)
    transaction.commit()

    if fresh:
        # connectTypesAndCategories(self) # TOOD: only when REI doctypes need to be added to ELAN categories
        # self.rei.correctAllDocTypes() # TODO: if the run display templates contains collections
        # with references to global doctypes, which need to be adapted to local doctypes.
        createREIGroups(self)
    self.reindexAll()

    # TODO: further initializations?

def copyRunDisplay(self, fresh):
    """

    @param self:
    @param fresh:
    @return:
    """
    if not fresh:
        return
    rei = self.rei
    from docpool.base.utils import _copyPaste
    _copyPaste(rei, self, safe=False)
    self.rei.setTitle(_("Run Display"))
    self.rei.reindexObject()
    # make sure the run display is first
    # TODO if more complex (e.g. second after 'esd')
    self.moveObject("rei", 0)




def dpRemoved(self):
    """
    @param self:
    @return:
    """
    # TODO:
    return

def createREIGroups(docpool):
    """
    Create Group for rei application access
    @param self: 
    @return: 
    """

    prefix = docpool.prefix or docpool.getId()
    prefix = str(prefix)
    title = docpool.Title()
    gtool = getToolByName(docpool, 'portal_groups')
    # Group for REI application rights
    props = {'allowedDocTypes': [], 'title': 'REI Users (%s)' % title,
             'description': 'Users with access to REI functions.',
             'dp': docpool.UID()}
    gtool.addGroup("%s_REIUsers" % prefix,
               properties=props)
    gtool.addPrincipalToGroup('%s_dpadmin' % prefix, '%s_REIUsers' % prefix)

    # Group for REI content administration - if needed, otherwise ignore...
    props = {'allowedDocTypes': [], 'title': 'REI Content Administrators (%s)' % title,
             'description': 'Responsible for the definition of structure and types.',
             'dp': docpool.UID()}
    gtool.addGroup("%s_REIContentAdministrators" % prefix,
                   properties=props)
    gtool.addPrincipalToGroup('%s_dpadmin' % prefix, '%s_REIContentAdministrators' % prefix)

    # Set REI role as a local role for the new group
    docpool.manage_setLocalRoles("%s_REIUsers" % prefix, ["REIUser"])
    # Set content admin access to config
    docpool.config.manage_setLocalRoles("%s_REIContentAdministrators" % prefix, ["Owner"])
    # and to navigation
    docpool.rei.manage_setLocalRoles("%s_REIContentAdministrators" % prefix, ["ContentAdmin"])