# -*- coding: UTF-8 -*-
from Products.Five.browser import BrowserView
from docpool.base.content.dpdocument import IDPDocument
from plone import api
from zope.component import getMultiAdapter
import logging

log = logging.getLogger(__name__)


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
        # FIXME: THIS DOES NOT WORK ! - also users which can add portal content in their group do only have these groups
        # roles = member.getRolesInContext(self.context)
        # read_only = ['Member', 'Authenticated', 'ELANUser', 'Reader']
        # can_change_pwd_roles = [r for r in roles if r not in read_only]
        # return bool(can_change_pwd_roles)

        # read only ELAN-Users
        # usually shared by multiple people
        if (member.getId()[-2:] =='-u') or (member.getId()[-5:] == '-info'):
            return False

        return True

    def is_rei_workflow(self, doc=None):
        """
        Checks if a rei workflow is activated on a dpdocument
        :param doc:
        :return:
        """
        if not doc:
            doc = self.context
        # Its a brain lets get the object
        if hasattr(doc, "getObject"):
           doc = doc.getObject()
        # rei workflow is only possible on dpdocument
        if not IDPDocument.providedBy(doc):
            log.info("Rei WF only possible on dpdocument")
            return
        wf_tool = api.portal.get_tool('portal_workflow')
        workflow = wf_tool.getWorkflowsFor(doc)[0]
        rei_wfs = ['rei_review_workflow_alternative', 'rei_review_workflow_standard']
        if workflow.id in rei_wfs:
            return True
        return False
