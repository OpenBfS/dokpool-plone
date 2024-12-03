from AccessControl import getSecurityManager
from Acquisition import aq_inner
from docpool.base.content.documentpool import IDocumentPool
from docpool.base.localbehavior.localbehavior import ILocalBehaviorSupport
from docpool.base.utils import get_content_area
from logging import getLogger
from plone import api
from plone.app.users.browser import userdatapanel
from plone.app.users.browser.register import BaseRegistrationForm
from plone.app.users.browser.schemaeditor import getFromBaseSchema
from plone.app.users.browser.userdatapanel import UserDataPanelAdapter
from plone.app.users.schema import IUserDataSchema
from plone.app.users.vocabularies import GroupIdVocabulary
from plone.base.interfaces import ISecuritySchema
from plone.base.interfaces.siteroot import IPloneSiteRoot
from plone.base.utils import safe_text
from plone.protect.interfaces import IDisableCSRFProtection
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.controlpanel.browser.usergroups import (
    UsersGroupsControlPanelView,
)
from Products.CMFPlone.utils import base_hasattr
from Products.CMFPlone.utils import normalizeString
from Products.PlonePAS.tools.groups import GroupsTool
from zope.component import getAdapter
from zope.component.globalregistry import provideAdapter
from zope.component.hooks import getSite
from zope.globalrequest import getRequest
from zope.interface import alsoProvides
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


logger = getLogger(__name__)


def email_as_username(self):
    # We need to set the right context here - the portal root
    return getAdapter(aq_inner(getSite()), ISecuritySchema).get_use_email_as_login()


def applyProperties(self, userid, data):
    # Set the current docpool reference to the data
    if base_hasattr(self.context, "myDocumentPool"):
        dp = self.context
        prefix = dp.prefix or dp.id
        data["dp"] = dp.UID()
        data["groups"].append(f"{prefix}_Members")

        BaseRegistrationForm._old_applyProperties(self, userid, data)


def addGroup(self, id, roles=[], groups=[], properties=None, REQUEST=None, *args, **kw):
    from docpool.base import DocpoolMessageFactory as _
    from docpool.base.utils import portalMessage

    logger.info("Adding group %s", id)
    ret = GroupsTool._old_addGroup(
        self,
        id,
        roles=roles,
        groups=groups,
        properties=properties,
        REQUEST=REQUEST,
        *args,
        **kw,
    )
    if not ret:
        return ret
    esd_uid = properties and properties.get("dp", None) or None
    if not esd_uid:
        esd_uid = kw.get("dp", None)
    title = properties and properties.get("title", None) or None
    if not title:
        title = kw.get("title", None)
    group_id = id
    g = self.getGroupById(group_id)
    if not esd_uid:
        esd_uid = g.getProperty("dp")
    if not title:
        title = g.getProperty("title")
    # print esd_uid
    context = self
    if esd_uid:
        catalog = getToolByName(self, "portal_catalog")
        result = catalog({"UID": esd_uid})
        if len(result) == 1:
            esd = result[0].getObject()
            context = esd.content
    if context.hasObject("Groups"):
        groups_container = context.Groups
        if not groups_container.hasObject(group_id):  # left over Group folder?
            logger.info("Creating group folder")
            gf = api.content.create(
                container=groups_container,
                type="GroupFolder",
                id=group_id,
                title=title,
            )
        else:
            logger.info("Old group folder in the way")
            portalMessage(
                context,
                _("There was an existing group folder of the same name. Please check!"),
                "error",
            )
            # get the new or old folder and edit it
            gf = groups_container._getOb(group_id)
            gf.title = title
        request = getRequest() or context.REQUEST
        if request:
            dp_app_state = api.content.get_view("dp_app_state", context, request)
            local_behaviors = dp_app_state.effectiveAppsHere()
            ILocalBehaviorSupport(gf).local_behaviors = list(local_behaviors)
        mtool = getToolByName(context, "portal_membership")
        mtool.setLocalRoles(gf, [group_id], "Owner")
        gf.update_immediately_addable_types()
        gf.reindexObject()
    return ret


def removeGroup(self, group_id, REQUEST=None):
    from docpool.base import DocpoolMessageFactory as _
    from docpool.base.utils import portalMessage

    # we should get this, before we delete...
    g = self.getGroupById(group_id)
    esd_uid = g.getProperty("dp")
    # print group_id, esd_uid
    # do the delete
    logger.info("Removing group %s", group_id)
    ret = GroupsTool._old_removeGroup(self, group_id, REQUEST)
    # Check if the group folder can be deleted
    context = self
    if esd_uid:
        catalog = getToolByName(self, "portal_catalog")
        result = catalog({"UID": esd_uid})
        if len(result) == 1:
            try:
                esd = result[0].getObject()
                context = get_content_area(esd)
            except KeyError:
                pass
    if base_hasattr(context, "Groups"):
        groups = context.Groups
        if groups.hasObject(group_id):
            g = groups._getOb(group_id)
            if g.canBeDeleted(principal_deleted=True):
                groups._delObject(group_id)
            else:
                portalMessage(
                    context,
                    _(
                        "The group folder could not be deleted because of protected documents. Please check!"
                    ),
                    "error",
                )
    return ret


def getUserDataSchema():
    portal = getSite()
    schema = getattr(portal, "_v_userdata_schema", None)
    if schema is None:
        portal._v_userdata_schema = schema = getFromBaseSchema(
            IUserDataSchema, form_name="In User Profile"
        )
        # as schema is a generated supermodel,
        # needed adapters can only be registered at run time
        provideAdapter(UserDataPanelAdapter, (IPloneSiteRoot,), schema)
        provideAdapter(UserDataPanelAdapter, (IDocumentPool,), schema)
    return schema


userdatapanel.getUserDataSchema = getUserDataSchema


def getGroupIds(self, context):
    site = getSite()
    groups_tool = getToolByName(site, "portal_groups")
    groups = groups_tool.listGroups()
    # Get group id, title tuples for each, omitting virtual group
    # 'AuthenticatedUsers'
    terms = []
    for g in groups:
        # Filter local groups

        if (
            context.getPortalTypeName() == "DocumentPool"
            and not g.getProperty("dp") == context.UID()
        ):
            continue
        if g.id.find("Members") > -1:
            continue
        if g.id == "AuthenticatedUsers":
            continue
        is_zope_manager = getSecurityManager().checkPermission(ManagePortal, context)
        if "Manager" in g.getRoles() and not is_zope_manager:
            continue

        group_title = safe_text(g.getGroupTitleOrName())
        if group_title != g.id:
            title = f"{group_title} ({g.id})"
        else:
            title = group_title
        terms.append(SimpleTerm(g.id, g.id, title))
    # Sort by title
    terms.sort(key=lambda x: normalizeString(x.title))
    return SimpleVocabulary(terms)


GroupIdVocabulary.__call__ = getGroupIds


def __csrfinit__(self, context, request):
    alsoProvides(request, IDisableCSRFProtection)
    UsersGroupsControlPanelView.__init__(self, context, request)
