import logging

from docpool.base.browser.dpdocument import (
    DPDocumentinlineView,
    DPDocumentlistitemView,
    DPDocumentprintView,
    DPDocumentView,
)
from docpool.base.content.simplefolder import SimpleFolder
from docpool.base.utils import deleteMemberFolders
from docpool.elan.config import ELAN_APP
from docpool.event.utils import getScenariosForCurrentUser
from plone.protect import CheckAuthenticator
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFPlone.CatalogTool import CatalogTool
from Products.CMFPlone.utils import aq_inner
from zExceptions import Forbidden

# from plone.app.controlpanel.usergroups import UsersOverviewControlPanel


# Patches for the dropdown menu to include personal and group folders


logger = logging.getLogger("plone.app.controlpanel")

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
        acl_users = getToolByName(context, "acl_users")
        mtool = getToolByName(context, "portal_membership")

        utils = getToolByName(context, "plone_utils")

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
            if hasattr(user, "email"):
                # If the email field was disabled (ie: non-writeable), the
                # property might not exist.
                if user.email != member.getProperty("email"):
                    utils.setMemberProperties(
                        member, REQUEST=context.REQUEST, email=user.email
                    )
                    utils.addPortalMessage(_("Changes applied."))

            # If reset password has been checked email user a new password
            pw = None
            if hasattr(user, "resetpassword"):
                if "Manager" in current_roles and not self.is_zope_manager:
                    raise Forbidden
                # ELAN: set password to userid
                pw = user.id

            roles = user.get("roles", [])
            if not self.is_zope_manager:
                # don't allow adding or removing the Manager role
                if ("Manager" in roles) != ("Manager" in current_roles):
                    raise Forbidden

            # Ideally, we would like to detect if any role assignment has
            # actually changed, and only then issue "Changes applied".
            acl_users.userFolderEditUser(
                user.id, pw, roles, member.getDomains(), REQUEST=context.REQUEST
            )

            if pw:
                pass  # ELAN: nothing more, password has already been set above

        if delete:
            self.deleteMembers(delete)
            deleteMemberFolders(context, delete)

        if users_with_reset_passwords:
            reset_passwords_message = _(
                "reset_passwords_msg",
                default="The following users have been sent an e-mail with link to reset their password: ${user_ids}",
                mapping={"user_ids": ", ".join(users_with_reset_passwords)},
            )
            utils.addPortalMessage(reset_passwords_message)
        if users_failed_reset_passwords:
            failed_passwords_message = _(
                "failed_passwords_msg",
                default="A password reset e-mail could not be sent to the following users: ${user_ids}",
                mapping={"user_ids": ", ".join(users_failed_reset_passwords)},
            )
            utils.addPortalMessage(failed_passwords_message, type="error")

        # TODO: issue message only if something actually has changed
        utils.addPortalMessage(_("Changes applied."))


# if not hasattr(UsersOverviewControlPanel, "original_manageUser"):
#    UsersOverviewControlPanel.original_manageUser = UsersOverviewControlPanel.manageUser
#    UsersOverviewControlPanel.manageUser = manageUser

# from docpool.users.browser.usergroups import UsersOverviewControlPanel as UOCP
# if not hasattr(UOCP, "original_manageUser"):
#    UOCP.original_manageUser = UsersOverviewControlPanel.original_manageUser
#    UOCP.manageUser = manageUser


def searchResults(self, REQUEST=None, **kw):
    has_search_text = kw.get("SearchableText", None)
    has_path = kw.get("path", None)
    # Internal means not a search by a user within search form
    isInternal = kw.get("object_provides", None)
    if has_search_text and isinstance(has_search_text, type({})):
        has_search_text = has_search_text.get("query", None)
        isInternal = True
    # user query, needs to be personalized
    if has_search_text and not isInternal:
        if has_path:
            path = kw["path"]
            # Make sure we only search in the content area
            kw["path"] = "%s/content" % path
        if has_search_text[-1] != "*":
            kw["SearchableText"] = has_search_text + "*"
        scns = getScenariosForCurrentUser(self)
        rqurl = ""
        if hasattr(self.REQUEST, "URL"):
            rqurl = self.REQUEST["URL"]
        isArchive = rqurl.find("/archive/") > -1
        if not isArchive:
            if scns:
                kw["scenarios"] = scns
            else:  # If we don't have a filter
                kw["scenarios"] = ["dontfindanything"]
    return self.original_searchResults(REQUEST, **kw)


if not hasattr(CatalogTool, "original_searchResults"):
    CatalogTool.original_searchResults = CatalogTool.searchResults
    CatalogTool.searchResults = searchResults
    CatalogTool.__call__ = searchResults


def getUserSelectedScenarios(self):
    """ """
    # FIXME
    from docpool.event.utils import getScenariosForCurrentUser

    usc = getScenariosForCurrentUser(self)
    return usc


# The folder needs an extension to determine the currently selected scenario.
if not hasattr(SimpleFolder, "getUserSelectedScenarios"):
    SimpleFolder.getUserSelectedScenarios = getUserSelectedScenarios


def elanobject(self):
    return self.context.doc_extension(ELAN_APP)


DPDocumentView.elanobject = elanobject
DPDocumentlistitemView.elanobject = elanobject
DPDocumentinlineView.elanobject = elanobject
DPDocumentprintView.elanobject = elanobject
