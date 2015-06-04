import logging
from Acquisition import aq_inner
from zExceptions import Forbidden
from itertools import chain

from Products.PluggableAuthService.interfaces.plugins import IRolesPlugin
from zope.component import getUtility
from plone.protect import CheckAuthenticator
from zope.component import getMultiAdapter
from Products.CMFCore.interfaces import ISiteRoot
from Products.CMFPlone import PloneMessageFactory as _
from Products.CMFCore.utils import getToolByName

from Products.CMFPlone.utils import normalizeString
from Products.CMFPlone.controlpanel.browser.usergroups_usersoverview import \
    UsersOverviewControlPanel as UOCP
from docpool.base.utils import deleteMemberFolders

logger = logging.getLogger('Products.CMFPlone')


class UsersOverviewControlPanel(UOCP):

    def manageUser(self, users=[], resetpassword=[], delete=[]):
        """
        Override in order to change password reset behavior: set password == userid
        and to delete user folders - if possible - when user is deleted
        """
        CheckAuthenticator(self.request)

        if users:
            context = aq_inner(self.context)
            acl_users = getToolByName(context, 'acl_users')
            mtool = getToolByName(context, 'portal_membership')
            regtool = getToolByName(context, 'portal_registration')

            utils = getToolByName(context, 'plone_utils')

            users_with_reset_passwords = []

            for user in users:
                # Don't bother if the user will be deleted anyway
                if user.id in delete:
                    continue

                member = mtool.getMemberById(user.id)
                current_roles = member.getRoles()
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
                    if not context.unrestrictedTraverse('@@overview-controlpanel').mailhost_warning():
                        pw = regtool.generatePassword()
                    else:
                        ######
                        # BfS: set password to userid                
                        pw = user.id

                roles = user.get('roles', [])
                if not self.is_zope_manager:
                    # don't allow adding or removing the Manager role
                    if ('Manager' in roles) != ('Manager' in current_roles):
                        raise Forbidden

                acl_users.userFolderEditUser(user.id, pw, roles, member.getDomains(), REQUEST=context.REQUEST)
                if pw:
                    context.REQUEST.form['new_password'] = pw
                    regtool.mailPassword(user.id, context.REQUEST)
                    users_with_reset_passwords.append(user.id)

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
            utils.addPortalMessage(_(u'Changes applied.'))
