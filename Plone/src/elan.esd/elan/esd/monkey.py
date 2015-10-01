# -*- coding: utf-8 -*-
from Products.PluggableAuthService.plugins import ZODBGroupManager
from Products.PlonePAS.plugins.group import GroupManager
from Products.CMFCore.utils import getToolByName
from plone.app.discussion.browser.conversation import ConversationView
from Products.ZCatalog.CatalogBrains import AbstractCatalogBrain, _GLOBALREQUEST_INSTALLED, getRequest
from Products.CMFPlone.utils import aq_get, aq_parent, aq_inner
from Products.CMFPlone.utils import log
#from plone.app.controlpanel.usergroups import UsersOverviewControlPanel
from Products.PlonePAS.tools.groups import GroupsTool
from Products.PlonePAS.tools.membership import MembershipTool

from Products.Archetypes.utils import shasattr


# Patches for the dropdown menu to include personal and group folders

from docpool.base.content.documentpool import DocumentPool
from elan.esd.testdata import deleteTestData, createGroupsAndUsers,\
    createTestDocuments
import datetime
from zope.interface import alsoProvides


from plone.protect import CheckAuthenticator
from zExceptions import Forbidden
import logging
from Products.CMFPlone import PloneMessageFactory as _
from elan.esd.utils import getScenariosForCurrentUser
from docpool.base.utils import deleteMemberFolders
from elan.esd.behaviors.elandocument import IELANDocument
from docpool.base.browser.dpdocument import DPDocumentView,\
    DPDocumentlistitemView, DPDocumentinlineView, DPDocumentprintView

logger = logging.getLogger('plone.app.controlpanel')

# Patch to change password reset behaviour. Set password to username.   
def manageUser(self, users=None, resetpassword=None, delete=None):
    if users is None:
        users = []
    if resetpassword is None:
        resetpassword = []
    if delete is None:
        delete = []

    CheckAuthenticator(self.request)

    if users:
        context = aq_inner(self.context)
        acl_users = getToolByName(context, 'acl_users')
        mtool = getToolByName(context, 'portal_membership')

        utils = getToolByName(context, 'plone_utils')

        users_with_reset_passwords = []
        users_failed_reset_passwords = []

        for user in users:
            # Don't bother if the user will be deleted anyway
            if user.id in delete:
                continue

            member = mtool.getMemberById(user.id)
            current_roles = member.getRoles()

            # TODO: is it still possible to change the e-mail address here?
            #       isn't that done on @@user-information now?
            # If email address was changed, set the new one
            if hasattr(user, 'email'):
                # If the email field was disabled (ie: non-writeable), the
                # property might not exist.
                if user.email != member.getProperty('email'):
                    utils.setMemberProperties(member, REQUEST=context.REQUEST, email=user.email)
                    utils.addPortalMessage(_(u'Changes applied.'))

            # If reset password has been checked email user a new password
            pw = None
            if hasattr(user, 'resetpassword'):
                if 'Manager' in current_roles and not self.is_zope_manager:
                    raise Forbidden
                # ELAN: set password to userid                
                pw = user.id

            roles = user.get('roles', [])
            if not self.is_zope_manager:
                # don't allow adding or removing the Manager role
                if ('Manager' in roles) != ('Manager' in current_roles):
                    raise Forbidden

            # Ideally, we would like to detect if any role assignment has
            # actually changed, and only then issue "Changes applied".
            acl_users.userFolderEditUser(user.id, pw, roles, member.getDomains(), REQUEST=context.REQUEST)

            if pw:
                pass # ELAN: nothing more, password has already been set above
            
        if delete:
            self.deleteMembers(delete)
            deleteMemberFolders(context, delete)

        if users_with_reset_passwords:
            reset_passwords_message = _(
                u"reset_passwords_msg",
                default=u"The following users have been sent an e-mail with link to reset their password: ${user_ids}",
                mapping={
                    u"user_ids" : ', '.join(users_with_reset_passwords),
                    },
                )
            utils.addPortalMessage(reset_passwords_message)
        if users_failed_reset_passwords:
            failed_passwords_message = _(
                u'failed_passwords_msg',
                default=u'A password reset e-mail could not be sent to the following users: ${user_ids}',
                mapping={
                    u'user_ids' : ', '.join(users_failed_reset_passwords),
                    },
                )
            utils.addPortalMessage(failed_passwords_message, type='error')

        # TODO: issue message only if something actually has changed
        utils.addPortalMessage(_(u'Changes applied.'))
  
    
#if not hasattr(UsersOverviewControlPanel, "original_manageUser"):
#    UsersOverviewControlPanel.original_manageUser = UsersOverviewControlPanel.manageUser
#    UsersOverviewControlPanel.manageUser = manageUser    

#from docpool.users.browser.usergroups import UsersOverviewControlPanel as UOCP
#if not hasattr(UOCP, "original_manageUser"):
#    UOCP.original_manageUser = UsersOverviewControlPanel.original_manageUser
#    UOCP.manageUser = manageUser


from Products.CMFPlone.CatalogTool import CatalogTool     
def searchResults(self, REQUEST=None, **kw):
    rqurl = self.REQUEST['URL']
    isArchive = rqurl.find('/archive/') > -1
    has_st = kw.get('SearchableText', None)
    has_path = kw.get('path', None)
    has_op = kw.get('object_provides', None)
    if has_st and not has_op: # user query, needs to be personalized
        if has_path:
            path = kw['path']
            kw['path'] = "%s/content" % path # Make sure we only search in one area
        if has_st[-1] != "*":
            kw['SearchableText'] = has_st + "*"
        scns = getScenariosForCurrentUser(self)
        if not isArchive:
            if scns:
                kw['scenarios'] = scns
            else: # If we don't have a filter
                kw['scenarios'] = ['dontfindanything']
    # print kw
    return self.original_searchResults(REQUEST, **kw)

if not hasattr(CatalogTool, "original_searchResults"):
    CatalogTool.original_searchResults = CatalogTool.searchResults
    CatalogTool.searchResults = searchResults
    CatalogTool.__call__ = searchResults

def createTestData(self, count=100, prune=False):
    """
    Creates 2 groups, 2 users, 2 scenarios and 'count' random documents.
    If 'prune' is True, then all existing (test)data will be deleted
    before it is created afresh.
    """
    if prune:
        deleteTestData(self)
    createGroupsAndUsers(self)
    try:
        self.contentconfig.scen.invokeFactory(id="scenario1", type_name="ELANScenario", title="Scenario 1", description="This is scenario 1", status="active", timeOfEvent=datetime.datetime.today())
    except:
        pass
    try:
        self.contentconfig.scen.invokeFactory(id="scenario2", type_name="ELANScenario", title="Scenario 2", description="This is scenario 2", status="active", exercise=True, timeOfEvent=datetime.datetime.today())
    except:
        pass
    createTestDocuments(self, count)
    self.reindexAll()
    return self.restrictedTraverse('@@view')()

if not hasattr(DocumentPool, "createTestData"):
    DocumentPool.createTestData = createTestData
    

def patched_quick_upload_file(self):
    from collective.quickupload.browser.quick_upload import QuickUploadFile
    result = QuickUploadFile._old_quick_upload_file(self) # Convention from collective.monkeypatcher
    request = self.request
    response = request.RESPONSE
    # we set another Content Type to correct problems with collective quickupload
    response.setHeader('Content-Type', 'text/json; charset=utf-8')
    return result

def elanobject(self):
    return IELANDocument(self.context)

DPDocumentView.elanobject = elanobject
DPDocumentlistitemView.elanobject = elanobject
DPDocumentinlineView.elanobject = elanobject
DPDocumentprintView.elanobject = elanobject