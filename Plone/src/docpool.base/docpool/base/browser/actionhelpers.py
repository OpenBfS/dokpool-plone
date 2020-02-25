# -*- coding: UTF-8 -*-
from Products.Five.browser import BrowserView
from plone import api
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
        read_only = ['Member', 'Authenticated', 'ELANUser', 'Reader']
        can_change_pwd_roles = [r for r in roles if r not in read_only]
        return bool(can_change_pwd_roles)

    def is_rei_workflow(self, doc=None):
        if not doc:
            doc = self.context
        wf_tool = api.portal.get_tool('portal_workflow')
        workflow = wf_tool.getWorkflowsFor(doc)[0]
        rei_wfs = ['rei_review_workflow_alternative', 'rei_review_workflow_standard']
        if workflow.id in rei_wfs:
            return True
        return False
