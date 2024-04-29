from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import setSecurityManager
from AccessControl.users import UnrestrictedUser as BaseUnrestrictedUser
from Acquisition import aq_get
from Acquisition import aq_inner
from plone import api
from plone.api.exc import CannotGetPortalError
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.log import log_exc
from Products.CMFPlone.utils import base_hasattr
from Products.CMFPlone.utils import parent
from zc.relation.interfaces import ICatalog
from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission

import logging
import re


log = logging.getLogger(__name__)

RARELY_USED_TYPES = {
    "Collection",
    "InfoFolder",
    "ReviewFolder",
    "CollaborationFolder",
    "PrivateFolder",
}

_punct_re = re.compile(r'[\t !"#$%&\'()*\-/<=>?@\[\\\]^_`{|},.:+]+')


def queryForObject(self, **kwa):
    """ """
    cat = getToolByName(self, "portal_catalog")
    # print kwa
    res = cat(kwa)
    if len(res) == 1:
        return res[0].getObject()
    else:
        return None


def queryForObjects(self, **kwa):
    """ """
    cat = getToolByName(self, "portal_catalog")
    # print kwa
    res = cat(kwa)
    return res


def is_group_folder(context):
    return "Groups" in context.getPhysicalPath() and context.getId() != "Groups"


def getAllowedDocumentTypes(self):
    """
    Determine the document types allowed for the current user in the current context
    """
    # if in a group folder, only allow the types for this group
    isGF = is_group_folder(self)

    grps = getGroupsForCurrentUser(self)
    dts = []
    # Determine the union of the allowed documents for each of the user's
    # groups
    if grps:
        for grp in grps:
            if not isGF or grp["id"] in self.getPhysicalPath():
                et = grp["etypes"]
                if et:
                    dts.extend(et)
    tids = list(set(dts))
    cat = getToolByName(self, "portal_catalog")
    esd = getDocumentPoolSite(self)
    # print tids
    res = cat(
        path="/".join(esd.getPhysicalPath()) + "/config",
        portal_type="DocType",
        id=tids,
        sort_on="sortable_title",
    )
    return res


def getAllowedDocumentTypesForGroup(self):
    """ """
    isGF = is_group_folder(self)
    dts = []
    if isGF:
        grp = self.getGroupOfFolder()
        if grp:
            allowed = grp.getProperty("allowedDocTypes", [])
            if allowed:
                dts.extend(allowed)
    else:
        return getAllowedDocumentTypes(self)
    tids = list(set(dts))
    cat = getToolByName(self, "portal_catalog")
    esd = getDocumentPoolSite(self)
    res = cat(
        path="/".join(esd.getPhysicalPath()) + "/config",
        portal_type="DocType",
        id=tids,
        sort_on="sortable_title",
    )
    return res


def getGroupsForCurrentUser(obj):
    """ """
    results = []

    # TODO: Make this method saner
    # find content-area through acquisition - duh...
    content = aq_get(obj, "content", None)
    if not content:
        return results

    gtool = getToolByName(obj, "portal_groups")
    # find folder "Groups" through acquisition  - duh...
    for item in content.Groups.getFolderContents():
        try:
            grp = gtool.getGroupById(item.id)
            etypes = grp.getProperty("allowedDocTypes", [])
            if etypes:
                title = grp.getProperty("title", "")
                results.append({"id": item.id, "title": title, "etypes": etypes})
        except Exception:
            log.info("Error getting group for %s", item.id, exc_info=True)
    return results


def deleteMemberFolders(self, member_ids):
    """ """
    for mid in member_ids:
        try:
            members = self.content.Members
            members.manage_delObjects([mid.replace("-", "--")])
        except Exception as e:
            log_exc(e)
            try:
                self.portal_membership.getMembersFolder().manage_delObjects(
                    [mid.replace("-", "--")]
                )
            except Exception as e:
                log_exc(e)


def getUserInfo(self, username=None):
    mtool = getToolByName(self, "portal_membership")
    if username:
        user = mtool.getMemberById(username)
    else:
        user = mtool.getAuthenticatedMember()
        # we can be called with a special permission context (execute_under_special_role)
        # therefore we need to get the correct user object
        user = mtool.getMemberById(user.getId())
    fullname = user.getProperty("fullname")
    userid = user.getId()
    if not fullname:
        fullname = userid
    primary_group = None
    if self.isInGroupFolder():
        primary_group = self.myGroup()
    return userid, fullname, primary_group


def portalMessage(self, msg, type="info"):
    ptool = getToolByName(self, "plone_utils")
    ptool.addPortalMessage(msg, type)


def back_references(target, relationship):
    """Return back references from source object on specified attribute_name"""
    return [
        i.from_object
        for i in api.relation.get(target=target, relationship=relationship)
    ]


def _copyPaste(source_obj, target_folder_obj, safe=True):
    result = api.content.copy(
        source=aq_inner(source_obj), target=target_folder_obj, safe_id=safe
    )
    if result:
        return result.getId()
    return None


def _cutPaste(source_obj, target_folder_obj, unique=False):
    if unique:
        if target_folder_obj.hasObject(source_obj.getId()):
            return
    result = api.content.move(source=source_obj, target=target_folder_obj, safe_id=True)


def getDocumentPoolSite(context):
    """ """
    # print context
    if getattr(context, "myDocumentPool", None) is not None:
        return context.myDocumentPool()
    else:
        return getSite()


class UnrestrictedUser(BaseUnrestrictedUser):
    """Unrestricted user that still has an id."""

    def getId(self):
        """Return the ID of the user."""
        return self.getUserName()


def execute_under_special_role(context, role, function, *args, **kwargs):
    """Execute code under special role priviledges.

    Example how to call::

        execute_under_special_role(portal, "Manager",
            doSomeNormallyNotAllowedStuff,
            source_folder, target_folder)

    @param context: Bei uns, um die PortalWurzel zu erreichen.

    @param function: Method to be called with special priviledges

    @param role: User role we are using for the security context when calling the priviledged code. For example, use "Manager".

    @param args: Passed to the function

    @param kwargs: Passed to the function
    """
    try:
        portal = api.portal.get()
    except CannotGetPortalError:
        log.warn("Could not get portal.")
        return
    sm = getSecurityManager()

    try:
        try:
            # Clone the current access control user and assign a new role for him/her
            # Note that the username (getId()) is left in exception tracebacks in error_log
            # so it is important thing to store
            tmp_user = UnrestrictedUser(sm.getUser().getId(), "", [role], "")

            # Act as user of the portal
            tmp_user = tmp_user.__of__(portal.acl_users)
            newSecurityManager(None, tmp_user)

            # Call the function
            return function(*args, **kwargs)

        except BaseException:
            # If special exception handlers are needed, run them here
            raise
    finally:
        # Restore the old security manager
        setSecurityManager(sm)


def checkLocalRole(context, role="Manager"):
    if api.user.is_anonymous():
        return False
    else:
        roles = api.user.get_roles(obj=context)
        # print "checking", roles
        if role in roles or "Manager" in roles:
            return True
        else:
            return False


# FIXME: performance optimization
def getActiveAllowedPersonalBehaviorsForDocument(doc, request):
    """
    Determine which behaviors are
    - configured for the object, which are also
    - allowed within the docpool and also
    - allowed for the user and
    - not currently filtered out.
    @param self:
    @return:
    """
    try:
        dp_app_state = getMultiAdapter((doc, request), name="dp_app_state")
        if is_personal(doc):  # no personal filtering in the content area
            permitted_apps = dp_app_state.appsEffectiveForObject(
                request, filtered=False
            )
        else:  # but in all other areas
            permitted_apps = dp_app_state.appsEffectiveForObject(request, filtered=True)
        permitted_apps.sort()
        # print "getActiveAllowed ", permitted_apps
        return permitted_apps
    except Exception as e:
        log_exc(e)
        return []


def setApplicationsForCurrentUser(self, apps):
    """

    @param context:
    @param apps:
    @return:
    """
    user = api.user.get_current()
    #    id = self.myDocumentPool().getId()
    # get currently activated apps
    #    current = user.getProperty("apps", default=[])
    #    new = []
    #    replaced = False
    #    for c in current:
    #        if c and c.startswith(id): # replace the selection for the docpool
    #            new.append("%s:%s" % (id, ",".join(apps)))
    #            replaced = True
    #        else:
    #            new.append(c) # otherwise keep the definition
    #    if not replaced: # if never set before for this docpool
    #        new.append("%s:%s" % (id, ",".join(apps)))
    # Keep it simple at the moment, maybe we need the stuff above later...
    new = apps
    # print "setApplicationsForCurrentUser ", new
    user.setMemberProperties({"apps": tuple(new)})


def activateAppFilter(self, activate=False):
    """

    @param self:
    @param activate:
    @return:
    """
    user = api.user.get_current()
    user.setMemberProperties({"filter_active": activate})


def extendOptions(context, request, options):
    brain = None
    cat = getToolByName(context, "portal_catalog")
    brains = cat(UID=context.UID())
    brain = None
    if len(brains) > 0:
        brain = brains[0]
    # print brain
    options["dpbrain"] = brain
    options["dpdoc"] = context
    options["myfolder_url"] = request.get("myfolder_url", "/")
    options["isOverview"] = int(request.get("isOverview", 0))
    options["isCollection"] = int(request.get("isCollection", 0))
    options["container_type"] = request.get("container_type")
    options["buttons"] = eval(request.get("buttons", "[]"))
    # print options
    return options


def getInheritedValue(behaviour_obj, key):
    parentObject = parent(behaviour_obj.context)
    if base_hasattr(parentObject, key):
        return getattr(parentObject, key)
    else:
        return getattr(behaviour_obj.context, key)


def possibleDocTypes(self):
    from docpool.base.vocabularies import DocTypeVocabularyFactory

    return [f"{a[0]}|{a[1]}" for a in DocTypeVocabularyFactory(self, raw=True)]


def possibleDocumentPools(self):
    dps = api.content.find(portal_type="DocumentPool", sort_on="sortable_title")
    res = [""]
    res.extend([f"{dp.UID}|{dp.Title}" for dp in dps])
    return res


def is_admin(context=None):
    roles = api.user.get_roles(obj=context)
    return "Manager" in roles or "Site Administrator" in roles


def is_contentadmin(context):
    if not hasattr(context, "myDocumentPool"):
        return False
    if is_admin(context):
        return True
    groups = api.user.get_current().getGroups()
    return any("ContentAdministrators" in g for g in groups)


def is_individual(context):
    return "Members" in context.getPhysicalPath() and context.getId() != "Members"


def is_personal(context):
    return "content" in context.getPhysicalPath() and context.getId() != "content"


def get_docpool_for_user(user=None):
    if user is None:
        user = api.user.get_current()

    # 1. Normal users have a dp assigned to them.
    if dp_uid := user.getProperty("dp"):
        if obj := api.content.get(UID=dp_uid):
            return obj

    # 2. No dp's or user without access to any dp.
    brains = api.content.find(portal_type="DocumentPool", sort_on="sortable_title")
    if not brains:
        return

    # 3. Some users have the id of a dp as prefix. Redirect to that.
    username = user.getUserName()
    user_prefix = username.split("_")[0]
    dokpool_prefix = user_prefix if username != user_prefix else None
    if dokpool_prefix:
        for brain in brains:
            obj = brain.getObject()
            if obj.myPrefix() == dokpool_prefix:
                return obj

    # 4. Fallback to first available dp
    return brains[0].getObject()
