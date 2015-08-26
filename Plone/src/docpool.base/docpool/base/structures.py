# -*- coding: utf-8 -*-
import transaction
from Products.Archetypes.utils import shasattr
from Products.CMFCore.utils import getToolByName
from zExceptions import BadRequest
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from Products.CMFPlone.utils import log, log_exc
from elan.esd import ELAN_EMessageFactory as _
from docpool.config.local import createContentArea, createUsers, createGroups,\
    setLocalRoles, navSettings



def docPoolAdded(obj, event=None):
    """
    """
    self = obj
    createContentArea(self, True)
    createUsers(self)
    createGroups(self)
    setLocalRoles(self)
    navSettings(self)
    self.reindexAll()
# documentpool.esdAdded = esdAdded

def docPoolRemoved(obj, event=None):
    """
    """
    self = obj
    deleteGroups(self)
    deleteUsers(self)
# documentpool.esdRemoved = esdRemoved

def deleteGroups(self):
    """
    """
    prefix = (hasattr(self, 'prefix') and self.prefix) or self.getId()
    prefix = str(prefix)
    gtool = getToolByName(self, 'portal_groups')
    # list existing groups and then delete them
    gids = gtool.getGroupIds()
    for gid in gids:
        if gid.startswith(prefix):
            gtool.removeGroup(gid) # also deletes the group folder via event subscribers

def deleteUsers(self):
    """
    """
    prefix = (hasattr(self, 'prefix') and self.prefix) or self.getId()
    prefix = str(prefix)
    mtool = getToolByName(self, 'portal_membership', None)
    # list all users for this ESD and delete them
    uids = mtool.listMemberIds()
    for uid in uids:
        if uid.startswith(prefix):
            try:
                mtool.deleteMembers([uid]) # also deletes the member folders
            except Exception, e:
                log_exc(e)


