# -*- coding: utf-8 -*-
from docpool.config import _
from docpool.config.utils import CHILDREN
from docpool.config.utils import createPloneObjects
from docpool.config.utils import ID
from docpool.config.utils import TITLE
from docpool.config.utils import TYPE
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from Products.Archetypes.utils import shasattr
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import log_exc


# General Docpool structures


def dpAdded(self):
    """
    """
    createContentArea(self, True)
    createUsers(self)
    createGroups(self)
    setLocalRoles(self)
    navSettings(self)
    copyDocTypes(self)
    self.reindexAll()


CONTENT_AREA = {
    TYPE: 'ContentArea',
    TITLE: u'Content Area',
    ID: 'content',
    "setExcludeFromNav": True,
    CHILDREN: [
        {TYPE: 'Users', TITLE: u'Members', ID: 'Members', CHILDREN: []},
        {TYPE: 'Groups', TITLE: u'Groups', ID: 'Groups', CHILDREN: []},
    ],
}


def createContentArea(self, fresh):
    """
    """
    createPloneObjects(self, [CONTENT_AREA], fresh)


def createUsers(self):
    # Set type for user folders
    mtool = getToolByName(self, "portal_membership")
    prefix = self.prefix or self.getId()
    prefix = str(prefix)
    title = self.Title()
    mtool.addMember(
        '%s_dpadmin' % prefix, 'DocPool Administrator (%s)' % title, [
            'Member'], []
    )
    dpadmin = mtool.getMemberById('%s_dpadmin' % prefix)
    dpadmin.setMemberProperties(
        {"fullname": 'DocPool Administrator (%s)' % title, "dp": self.UID()}
    )
    dpadmin.setSecurityProfile(password="admin")


def setLocalRoles(self):
    """
    Normal local members: Reader
    Administrators: Site Administrator
    ContentAdministrators: Reviewer
    Receivers: Owner, Editor
    Senders: Contributor
    """
    prefix = self.prefix or self.getId()
    prefix = str(prefix)
    self.manage_setLocalRoles("%s_Members" % prefix, ["Reader"])
    self.manage_setLocalRoles(
        "%s_Administrators" %
        prefix, ["Site Administrator"])


def createGroups(self):
    # We need local groups for
    # - General access to the ESD
    # - Administration
    # - Content Administration
    # - Receiving content from others
    # - Sending content to others

    prefix = self.prefix or self.getId()
    prefix = str(prefix)
    title = self.Title()
    gtool = getToolByName(self, 'portal_groups')
    props = {
        'allowedDocTypes': [],
        'title': 'Members (%s)' % title,
        'description': 'Users of the DocPool.',
        'dp': self.UID(),
    }
    gtool.addGroup("%s_Members" % prefix, properties=props)
    gtool.addPrincipalToGroup('%s_dpadmin' % prefix, '%s_Members' % prefix)
    props = {
        'allowedDocTypes': [],
        'title': 'Administrators (%s)' % title,
        'description': 'Responsible for the administration of the DocPool.',
        'dp': self.UID(),
    }
    gtool.addGroup("%s_Administrators" % prefix, properties=props)
    gtool.addPrincipalToGroup(
        '%s_dpadmin' %
        prefix,
        '%s_Administrators' %
        prefix)


def navSettings(self):
    IExcludeFromNavigation(self.content).exclude_from_nav = True
    self.content.reindexObject()


def copyDocTypes(self):
    """
    """
    if shasattr(self, "config", acquire=False):
        return
    config = self.config
    from docpool.base.utils import _copyPaste

    _copyPaste(config, self)
    self.config.setTitle(_("Configuration"))
    self.config.reindexObject()
    self.config.dtypes.setTitle(_("Document Types"))
    self.config.dtypes.reindexObject()


def dpRemoved(self):
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
            gtool.removeGroup(
                gid
            )  # also deletes the group folder via event subscribers


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
                mtool.deleteMembers([uid])  # also deletes the member folders
            except Exception as e:
                log_exc(e)
