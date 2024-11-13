from docpool.base.content.documentpool import APPLICATIONS_KEY
from docpool.base.utils import _copyPaste
from docpool.rodos import DocpoolMessageFactory as _
from docpool.rodos.config import RODOS_APP
from plone import api
from plone.base.utils import get_installer
from Products.CMFCore.utils import getToolByName
from zope.annotation.interfaces import IAnnotations

import transaction


def dpAdded(self, reindex=True):
    """
    @param self:
    @return:

    """
    portal = api.portal.get()
    installer = get_installer(portal)
    if not installer.is_product_installed("docpool.rodos"):
        raise RuntimeError("docpool.rodos is not installed!")
    annotations = IAnnotations(self)
    fresh = RODOS_APP not in annotations[APPLICATIONS_KEY]
    if fresh:
        annotations[APPLICATIONS_KEY].append(RODOS_APP)
        copyRodosContent(self, fresh)
        # connectTypesAndCategories(self) # TOOD: only when RODOS doctypes need to be added to ELAN categories
        # self.rodos.correctAllDocTypes() # TODO: if the run display templates contains collections
        # with references to global doctypes, which need to be adapted to local
        # doctypes.
        createRodosGroups(self)
        transaction.commit()

    # No duplicate work when adding rodos to more dokpools in a upgrade-step
    if reindex:
        self.reindexAll()


def copyRodosContent(dokpool, fresh):
    """

    @param self: DocumentPool
    @param fresh: bool
    @return:
    """
    if not fresh:
        return

    portal = api.portal.get()
    _copyPaste(portal["potentially-affected-areas"], dokpool, safe=False)
    _copyPaste(portal["projections"], dokpool, safe=False)
    dokpool["potentially-affected-areas"].reindexObject()
    dokpool["projections"].reindexObject()


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
    gtool = getToolByName(docpool, "portal_groups")
    # Group for Rodos application rights
    props = {
        "allowedDocTypes": [],
        "title": "Rodos Users (%s)" % title,
        "description": "Users with access to Rodos functions.",
        "dp": docpool.UID(),
    }
    gtool.addGroup("%s_RodosUsers" % prefix, properties=props)
    gtool.addPrincipalToGroup("%s_dpadmin" % prefix, "%s_RodosUsers" % prefix)

    # Group for Rodos content administration - if needed, otherwise ignore...
    props = {
        "allowedDocTypes": [],
        "title": "Rodos Content Administrators (%s)" % title,
        "description": "Responsible for the definition of structure and types.",
        "dp": docpool.UID(),
    }
    gtool.addGroup("%s_RodosContentAdministrators" % prefix, properties=props)
    gtool.addPrincipalToGroup(
        "%s_dpadmin" % prefix, "%s_RodosContentAdministrators" % prefix
    )

    # Set Rodos role as a local role for the new group
    docpool.manage_setLocalRoles("%s_RodosUsers" % prefix, ["RodosUser"])
    # Set content admin access to config
    docpool.config.manage_setLocalRoles(
        "%s_RodosContentAdministrators" % prefix, ["Owner"]
    )
    # and to navigation
    docpool["potentially-affected-areas"].manage_setLocalRoles(
        "%s_RodosContentAdministrators" % prefix, ["ContentAdmin"]
    )
    docpool["projections"].manage_setLocalRoles(
        "%s_RodosContentAdministrators" % prefix, ["ContentAdmin"]
    )
