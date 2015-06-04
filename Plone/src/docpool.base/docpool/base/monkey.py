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


