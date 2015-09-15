# -*- coding: utf-8 -*-
from Products.PluggableAuthService.plugins import ZODBGroupManager
from Products.PlonePAS.plugins.group import GroupManager
from Products.CMFCore.utils import getToolByName
from plone.app.discussion.browser.conversation import ConversationView
from Products.ZCatalog.CatalogBrains import AbstractCatalogBrain, _GLOBALREQUEST_INSTALLED, getRequest
from Acquisition import aq_get, aq_parent, aq_inner
from Products.CMFPlone.utils import log, log_exc
#from plone.app.controlpanel.usergroups import UsersOverviewControlPanel
from Products.PlonePAS.tools.groups import GroupsTool
from Products.PlonePAS.tools.membership import MembershipTool

from Products.Archetypes.utils import shasattr

from plone.api import user
from zExceptions import BadRequest

# Patches for the automatic creation of group folders
    
def enabled(self):
    """
    Needs to be patched, so that comments are enabled for the DPDocument type.
    Normally, they cannot be enabled for a folderish type.
    """
    # print "enabled"
    from docpool.base.content.dpdocument import IDPDocument
    context = aq_inner(self.context)
    if IDPDocument.providedBy(context):
        if not context.isArchive():
            return True
        else:
            return False
    else:
        return self.original_enabled()
    
if not hasattr(ConversationView, "original_enabled"):
    ConversationView.original_enabled = ConversationView.enabled
    ConversationView.enabled = enabled

def getURL(self, relative=0, original=False):
    """
    Patched so we can provide special URLs for ELAN documents in listings such as livesearch.
    Also we make sure that sections don't get an URL, so they are not linked to in the navigation.
    """
    request = aq_get(self, 'REQUEST', None)
    if request is None and _GLOBALREQUEST_INSTALLED:
        request = getRequest()
    if (not original) and self.portal_type == 'DPDocument':
        if self.cat_path:
            # This is it: we use the path of the category
            return "%s/@@dview?d=%s&disable_border=1" % (self.cat_path, self.UID)
    # The following leads to errors in the folder_contents view of esd.
    #if (not original) and self.portal_type == "ELANSection":
    #    return None
    
    # This is the normal implementation
    return request.physicalPathToURL(self.getPath(), relative)

if not hasattr(AbstractCatalogBrain, "original_getURL"):
    AbstractCatalogBrain.original_getURL = AbstractCatalogBrain.getURL
    AbstractCatalogBrain.getURL = getURL

