from Acquisition import aq_inner
from zope.component import getAdapter
from Products.CMFPlone.interfaces import ISecuritySchema
from zope.component.hooks import getSite
from Products.Archetypes.utils import shasattr
from plone.app.users.browser.register import BaseRegistrationForm
from Products.PlonePAS.tools.groups import GroupsTool
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.log import log

def email_as_username(self):
    # We need to set the right context here - the portal root
    return getAdapter(aq_inner(getSite()), ISecuritySchema).get_use_email_as_login()



def applyProperties(self, userid, data):
    # we need to add the correct DP reference to the data
    if shasattr(self.context, "myDocumentPool"):
        dp = self.context
        prefix = dp.prefix or dp.getId()
        prefix = str(prefix)
        data['dp'] = dp.UID()
        data['groups'].append("%s_Members" % prefix)
        
        BaseRegistrationForm._old_applyProperties(self, userid, data)



def addGroup(self, id, roles=[], groups=[], properties=None,
                 REQUEST=None, *args, **kw):
    from docpool.base import ELAN_EMessageFactory as _
    from docpool.base.utils import portalMessage
    log("Adding group %s" % id)
    ret = GroupsTool._old_addGroup(self, id, roles=roles, groups=groups, properties=properties,
                 REQUEST=REQUEST)
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
    #print esd_uid
    context = self
    if esd_uid:
        catalog = getToolByName(self, 'portal_catalog')
        result  = catalog({'UID' : esd_uid})
        if len(result) == 1:
            esd = result[0].getObject()
            context = esd.content
    #print context
    if hasattr(context, "Groups"):
        groups = context.Groups
        if not groups.hasObject(group_id):  # left over Group folder?
            log("Creating group folder")
            groups.invokeFactory("GroupFolder", id=group_id, title=title) # if not we create a new folder
        else:
            log("Old group folder in the way")
            portalMessage(context, _("There was an existing group folder of the same name. Please check!"), "error")
            gf = groups._getOb(group_id) # get the new or old folder and edit it
            gf.setTitle(title)
            gf.reindexObject()
        gf = groups._getOb(group_id) # get the new or old folder and edit it
        mtool = getToolByName(context, "portal_membership")
        mtool.setLocalRoles(gf,[group_id],'Owner')
    return ret

def removeGroup(self, group_id, REQUEST=None):
    from docpool.base import ELAN_EMessageFactory as _
    from docpool.base.utils import portalMessage
    # we should get this, before we delete...
    g = self.getGroupById(group_id)
    esd_uid = g.getProperty("dp")
    # print group_id, esd_uid
    # do the delete
    log("Removing group %s" % group_id)
    ret = GroupsTool._old_removeGroup(self, group_id, REQUEST)
    # Check if the group folder can be deleted
    context = self
    if esd_uid:
        catalog = getToolByName(self, 'portal_catalog')
        result  = catalog({'UID' : esd_uid})
        if len(result) == 1:
            esd = result[0].getObject()
            context = esd.content
    if shasattr(context, "Groups"):
        groups = context.Groups
        if groups.hasObject(group_id):
            g = groups._getOb(group_id)
            if g.canBeDeleted(principal_deleted=True):
                groups._delObject(group_id)
            else:
                portalMessage(context, _("The group folder could not be deleted because of protected documents. Please check!"), "error")
    return ret

