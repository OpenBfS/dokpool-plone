from docpool.base.config import BASE_APP
from docpool.base.content.documentpool import APPLICATIONS_KEY
from docpool.config import _
from docpool.config.utils import CHILDREN
from docpool.config.utils import createPloneObjects
from docpool.config.utils import ID
from docpool.config.utils import TITLE
from docpool.config.utils import TYPE
from logging import getLogger
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import base_hasattr
from Products.CMFPlone.utils import log_exc
from zope.annotation.interfaces import IAnnotations

logger = getLogger(__name__)

# General Docpool structures


def dpAdded(self):
    """ """
    annotations = IAnnotations(self)
    fresh = BASE_APP not in annotations[APPLICATIONS_KEY]
    if fresh:
        annotations[APPLICATIONS_KEY].append(BASE_APP)

    createContentArea(self, fresh)
    createUsers(self)
    createGroups(self)
    setLocalRoles(self)
    navSettings(self)
    copyDocTypes(self)
    self.reindexAll()


CONTENT_AREA = {
    TYPE: "ContentArea",
    TITLE: "Benutzer/Gruppen/Transferordner",
    ID: "content",
    "setExcludeFromNav": True,
    CHILDREN: [
        {TYPE: "Users", TITLE: "Benutzer", ID: "Members", CHILDREN: []},
        {TYPE: "Groups", TITLE: "Gruppen", ID: "Groups", CHILDREN: []},
    ],
}


def createContentArea(self, fresh):
    """ """
    createPloneObjects(self, [CONTENT_AREA], fresh)


def createUsers(self):
    # Set type for user folders
    mtool = getToolByName(self, "portal_membership")
    prefix = self.prefix or self.getId()
    prefix = str(prefix)
    title = self.Title()
    mtool.addMember(
        "%s_dpadmin" % prefix, "DocPool Administrator (%s)" % title, ["Member"], []
    )
    dpadmin = mtool.getMemberById("%s_dpadmin" % prefix)
    dpadmin.setMemberProperties(
        {"fullname": "DocPool Administrator (%s)" % title, "dp": self.UID()}
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
    self.manage_setLocalRoles("%s_Administrators" % prefix, ["Site Administrator"])


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
    gtool = getToolByName(self, "portal_groups")
    props = {
        "allowedDocTypes": [],
        "title": "Members (%s)" % title,
        "description": "Users of the DocPool.",
        "dp": self.UID(),
    }
    gtool.addGroup("%s_Members" % prefix, properties=props)
    gtool.addPrincipalToGroup("%s_dpadmin" % prefix, "%s_Members" % prefix)
    props = {
        "allowedDocTypes": [],
        "title": "Administrators (%s)" % title,
        "description": "Responsible for the administration of the DocPool.",
        "dp": self.UID(),
    }
    gtool.addGroup("%s_Administrators" % prefix, properties=props)
    gtool.addPrincipalToGroup("%s_dpadmin" % prefix, "%s_Administrators" % prefix)


def navSettings(self):
    IExcludeFromNavigation(self.content).exclude_from_nav = True
    self.content.reindexObject()


def copyDocTypes(self):
    """ """
    if base_hasattr(self, "config"):
        return
    config = self.config
    from docpool.base.utils import _copyPaste

    _copyPaste(config, self)
    self.config.setTitle(_("Konfiguration"))
    self.config.reindexObject()
    self.config.dtypes.setTitle(_("Dokumenttypen"))
    self.config.dtypes.reindexObject()


def dpRemoved(self):
    deleteGroups(self)
    deleteUsers(self)
    # documentpool.esdRemoved = esdRemoved


def deleteGroups(self):
    """ """
    prefix = (hasattr(self, "prefix") and self.prefix) or self.getId()
    prefix += "_"
    gtool = getToolByName(self, "portal_groups")
    # list existing groups and then delete them
    gids = gtool.getGroupIds()
    for gid in gids:
        if gid.startswith(prefix):
            # also deletes the group folder via monkeypatched removeGroup
            gtool.removeGroup(gid)


def deleteUsers(self):
    """ """
    prefix = (hasattr(self, "prefix") and self.prefix) or self.getId()
    prefix += "_"
    mtool = getToolByName(self, "portal_membership", None)
    # Get all users for this ESD and delete them
    uids = mtool.listMemberIds()
    member_ids = [i for i in uids if i.startswith(prefix)]
    logger.info("Deleting members: %s" % member_ids)
    # This also deletes the member folders and reindexes security
    if member_ids:
        mtool.deleteMembers(member_ids=member_ids)
