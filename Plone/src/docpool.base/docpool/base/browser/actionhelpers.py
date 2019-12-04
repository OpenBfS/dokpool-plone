# -*- coding: UTF-8 -*-
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter


class ActionHelpers(BrowserView):

    def can_change_password(self):
        portal_state = getMultiAdapter(
            (self.context, self.request), name=u'plone_portal_state')

        member = portal_state.member()
        # IMIS-Users uses SSO and cannot change their password
        if member.getId()[:2] == 'i-':
            return False

        # User with only these roles should not change their password.
        # They are usually shared by multiple people.
        roles = member.getRolesInContext(self.context)
        read_only = ['Member', 'Authenticated', 'ELANUser']
        can_change_pwd_roles = [r for r in roles if r not in read_only]
        return bool(can_change_pwd_roles)
