# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
import transaction
from docpool.rodos import DocpoolMessageFactory as _




def dpAdded(self):
    """
    @param self: 
    @return: 
        
    """
    fresh = True
    if self.hasObject("rodos"):
        fresh = False # It's a reinstall

    copyRunDisplay(self, fresh)
    transaction.commit()

    if fresh:
        # connectTypesAndCategories(self) # TOOD: only when RODOS doctypes need to be added to ELAN categories
        # self.rodos.correctAllDocTypes() # TODO: if the run display templates contains collections
        # with references to global doctypes, which need to be adapted to local doctypes.
        createRodosGroups(self)
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
    rodos = self.rodos
    from docpool.base.utils import _copyPaste
    _copyPaste(rodos, self, safe=False)
    self.rodos.setTitle(_("Run Display"))
    self.rodos.reindexObject()
    # make sure the run display is first
    # TODO if more complex (e.g. second after 'esd')
    self.moveObject("rodos", 0)




def dpRemoved(self):
    """
    @param self:
    @return:
    """
    # TODO:
    return

def createRodosGroups(docpool):
    """
    Create Group for rodos application access
    @param self: 
    @return: 
    """

    prefix = docpool.prefix or docpool.getId()
    prefix = str(prefix)
    title = docpool.Title()
    gtool = getToolByName(docpool, 'portal_groups')
    # Group for Rodos application rights
    props = {'allowedDocTypes': [], 'title': 'Rodos Users (%s)' % title,
             'description': 'Users with access to Rodos functions.',
             'dp': docpool.UID()}
    gtool.addGroup("%s_RodosUsers" % prefix,
               properties=props)
    gtool.addPrincipalToGroup('%s_dpadmin' % prefix, '%s_RodosUsers' % prefix)

    # Group for Rodos content administration - if needed, otherwise ignore...
    props = {'allowedDocTypes': [], 'title': 'Rodos Content Administrators (%s)' % title,
             'description': 'Responsible for the definition of structure and types.',
             'dp': docpool.UID()}
    gtool.addGroup("%s_RodosContentAdministrators" % prefix,
                   properties=props)
    gtool.addPrincipalToGroup('%s_dpadmin' % prefix, '%s_RodosContentAdministrators' % prefix)

    # Set Rodos role as a local role for the new group
    docpool.manage_setLocalRoles("%s_RodosUsers" % prefix, ["RodosUser"])
    # Set content admin access to config
    docpool.config.manage_setLocalRoles("%s_RodosContentAdministrators" % prefix, ["Owner"])
    # and to navigation
    docpool.rodos.manage_setLocalRoles("%s_RodosContentAdministrators" % prefix, ["ContentAdmin"])
