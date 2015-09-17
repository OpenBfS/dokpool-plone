from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import aq_inner
from Products.Archetypes.utils import shasattr
from Products.CMFPlone.log import log_exc
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission
from zc.relation.interfaces import ICatalog
from Products.CMFPlone.utils import parent
from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager, setSecurityManager
from AccessControl.User import UnrestrictedUser as BaseUnrestrictedUser
from zope.component.hooks import getSite
from plone import api
from zope.component import getMultiAdapter

def queryForObject(self, **kwa):
    """
    """
    cat = getToolByName(self, "portal_catalog")
    # print kwa
    res = cat(kwa)
    if len(res) == 1:
        return res[0].getObject()
    else:
        return None

def queryForObjects(self, **kwa):
    """
    """
    cat = getToolByName(self, "portal_catalog")
    #print kwa
    res = cat(kwa)
    return res
    
def getAllowedDocumentTypes(self):
    """
    Determine the ELAN document types allowed for the current user in the current context
    """
    # if in a group folder, only allow the types for this group
    isGF = self.isGroupFolder()
        
    grps = getGroupsForCurrentUser(self)
    dts = []
    # Determine the union of the allowed documents for each of the user's groups
    if grps:
        for grp in grps:
            if not isGF or grp['id'] in self.getPhysicalPath():
                et = grp['etypes']
                if et:
                    dts.extend(et)
    tids = list(set(dts))
    cat = getToolByName(self, "portal_catalog")
    esd = getDocumentPoolSite(self)
    # print tids
    res = cat(path="/".join(esd.getPhysicalPath()) + "/config", portal_type = 'DocType', id=tids, sort_on="sortable_title")
    return res

def getAllowedDocumentTypesForGroup(self):
    """
    """
    isGF = self.isGroupFolder()
    dts = []
    if isGF:
        grp = self.getGroupOfFolder()
        dts.extend(grp.getProperty('allowedDocTypes', []))
    else:
        return getAllowedDocumentTypes(self)
    tids = list(set(dts))
    cat = getToolByName(self, "portal_catalog")
    esd = getDocumentPoolSite(self)
    res = cat(path="/".join(esd.getPhysicalPath()) + "/config", portal_type = 'DocType', id=tids, sort_on="sortable_title")
    return res

# def getActiveScenarios(self):
#     cat = getToolByName(self, "portal_catalog")
#     esd = getDocumentPoolSite(self)
#     res = cat(path="/".join(esd.getPhysicalPath()) + "/contentconfig", portal_type = 'ELANScenario', dp_type="active", sort_on="modified", sort_order="reverse")
#     return res
# 
# def getOpenScenarios(self):
#     cat = getToolByName(self, "portal_catalog")
#     esd = getDocumentPoolSite(self)
#     res = cat(path="/".join(esd.getPhysicalPath()) + "/contentconfig", portal_type = 'ELANScenario', dp_type=["active","inactive"], sort_on="created", sort_order="reverse")
#     return res
# 
# def getAvailableCategories(self):
#     cat = getToolByName(self, "portal_catalog")
#     esd = getDocumentPoolSite(self)
#     res = cat(path="/".join(esd.getPhysicalPath()) + "/esd", portal_type = 'ELANDocCollection', dp_type=["active"], sort_on="sortable_title")
#     return res
# 
# def getScenariosForCurrentUser(self):
#     """
#     """
#     mtool = getToolByName(self, "portal_membership")
#     user = mtool.getAuthenticatedMember()
#     sc = user.getProperty("scenarios", None)
#     if not sc:
#         # intented implementation: use the latest active scenario
#         #a_s = getActiveScenarios(self)
#         #sc = len(a_s) > 0 and [ a_s[0].Title ] or []
#         # temporarily: no filter
#         return []
#     return list(sc)
# 
# def getCategoriesForCurrentUser(self):
#     mtool = getToolByName(self, "portal_membership")
#     user = mtool.getAuthenticatedMember()
#     cs = user.getProperty("categories", None)
#     if not cs:
#         return []
#     return list(cs)
# 
# def setScenariosForCurrentUser(self, scenarios):
#     """
#     """
#     mtool = getToolByName(self, "portal_membership")
#     user = mtool.getAuthenticatedMember()
#     user.setMemberProperties({"scenarios": scenarios})
#     
# def setCategoriesForCurrentUser(self, cats):
#     """
#     """
#     if type(cats) == type(""):
#         cats = [cats]
#     mtool = getToolByName(self, "portal_membership")
#     user = mtool.getAuthenticatedMember()
#     user.setMemberProperties({"categories": cats})

    
def getGroupsForCurrentUser(self, user=None):
    """
    """
    if not user:
        mtool = getToolByName(self, "portal_membership")
        user = mtool.getAuthenticatedMember()
    g = self.content.Groups
#    gpath = "/".join(g.getPhysicalPath())
    gordner = g.getFolderContents()
    
    #print groups
    gtool = getToolByName(self, "portal_groups")
    res = []
    for g in gordner:
        try:
            grp = gtool.getGroupById(g.id)
            etypes = grp.getProperty('allowedDocTypes', []) 
            title = grp.getProperty('title','')
            res.append({'id': g.id, 'title' : title, 'etypes' : etypes})
        except Exception, e:
            log_exc(e)
    return res

def deleteMemberFolders(self, member_ids):
    """
    """
    for mid in member_ids:
        try:
            # TODO
            self.portal_membership.getMembersFolder().manage_delObjects([mid.replace("-","--")])
        except Exception, e:
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
    #groups = [g for g in getGroupsForCurrentUser(self, user) if g['etypes']]
    fullname = user.getProperty("fullname")
    userid = user.getId()
    if not fullname:
        fullname = userid
    primary_group = None
    #if len(groups) > 0:
    #    # Normal ELAN user with at least one group
    #    primary_group = groups[0]['title']
    if self.isInGroupFolder():
        # determine the group
        primary_group = self.myGroup()
    return userid, fullname, primary_group

# def getRelativePath(obj):
#     if obj.isArchive():
#         portal_path_length = len( obj.myELANArchive().getPhysicalPath() )
#         content_path = obj.getPhysicalPath()
#         return "/".join(content_path[portal_path_length:])
#     else:
#         # print obj
#         # print obj.portal_url()
#         # print obj.portal_url.getRelativeUrl(obj)
#         return obj.portal_url.getRelativeUrl(obj)

def portalMessage(self, msg, type):
    ptool = getToolByName(self, "plone_utils")
    ptool.addPortalMessage(msg, type)
    
def back_references(source_object, attribute_name):
    """ Return back references from source object on specified attribute_name """
    try:
        catalog = getUtility(ICatalog)
        intids = getUtility(IIntIds)
        result = []
        # print 'back_reference ',  intids.getId(aq_inner(source_object))
        for rel in catalog.findRelations(
                                dict(to_id=intids.getId(aq_inner(source_object)),
                                     from_attribute=attribute_name)
                                ):
            # print rel
            obj = intids.queryObject(rel.from_id)
            # print 'treffer ',  obj
            if obj is not None and checkPermission('zope2.View', obj):
                result.append(obj)
        return result
    except Exception, e:
        log_exc(e)
        return []
    
def _copyPaste(source_obj, target_folder_obj):
    source_id = source_obj.getId()
    p = parent(source_obj)
    cb_copy_data = p.manage_copyObjects(source_obj.getId())
    result = target_folder_obj.manage_pasteObjects(cb_copy_data)
    if result:
        for r in result:
            if r['id'] == source_id:
                return r['new_id']
    return None

def _cutPaste(source_obj, target_folder_obj, unique=False):
    if unique:
        if target_folder_obj.hasObject(source_obj.getId()):
            return
    p = parent(source_obj)
    cb_copy_data = p.manage_cutObjects(source_obj.getId())
    result = target_folder_obj.manage_pasteObjects(cb_copy_data)
    
def getDocumentPoolSite(context):
    """
    """
    # print context
    if shasattr(context, "myDocumentPool", acquire=True):
        return context.myDocumentPool()
    else:
        return getSite()

def possibleDocumentPools(context):
    cat = getToolByName(context, 'portal_catalog')
    dps = cat.unrestrictedSearchResults({"portal_type":"DocumentPool", "sort_on": "sortable_title"})
    return dps

class UnrestrictedUser(BaseUnrestrictedUser):
    """Unrestricted user that still has an id.
    """
    def getId(self):
        """Return the ID of the user.
        """
        return self.getUserName()

def execute_under_special_role(context, role, function, *args, **kwargs):
    """ Execute code under special role priviledges.

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

    portal_state = getMultiAdapter((context, context.REQUEST), name=u'plone_portal_state')
    portal = portal_state.portal()

    sm = getSecurityManager()

    try:
        try:

            # Clone the current access control user and assign a new role for him/her
            # Note that the username (getId()) is left in exception tracebacks in error_log
            # so it is important thing to store
            tmp_user = UnrestrictedUser(
              sm.getUser().getId(),
               '', [role],
               ''
           )

            # Act as user of the portal
            tmp_user = tmp_user.__of__(portal.acl_users)
            newSecurityManager(None, tmp_user)

            # Call the function
            return function(*args, **kwargs)

        except:
            # If special exception handlers are needed, run them here
            raise
    finally:
        # Restore the old security manager
        setSecurityManager(sm)
        
def checkLocalRole(context, role='Manager'):
    if api.user.is_anonymous():
        return False
    else:
        roles = api.user.get_roles(obj=context)
        #print "checking", roles
        if role in roles or 'Manager' in roles:
            return True
        else:
            return False
    