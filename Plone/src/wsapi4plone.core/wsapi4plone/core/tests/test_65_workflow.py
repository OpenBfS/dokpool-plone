# -*- coding: utf-8 -*-
import unittest
import xmlrpclib

from zope.component import getUtility
from ZPublisher.xmlrpc import Response
from ZPublisher.tests.test_xmlrpc import FauxResponse

from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.PloneTestCase import PloneTestCase

from wsapi4plone.core.browser.workflow import Workflow

class TestWorkflow(PloneTestCase.PloneTestCase):
    """What kind of content-types do we have the ability to add using the
    'get_types' call."""

    def afterSetUp(self):
        self.setRoles(['Member', 'Manager'])

    def test_anonymous_get_workflow(self):
        # Setup the context variable.
        fp = self.portal['front-page']
        # First, setup the call results.
        resp = Response(FauxResponse())
        wf = Workflow(fp, '')
        self.logout()
        wf_data = wf.get_workflow()
        resp.setBody(wf_data)
        wf_body = resp._body
        wf_resp, method = xmlrpclib.loads(wf_body)
        wf_results = wf_resp[0]
        # Now, get the results directly from the tool.
        portal_workflow = getToolByName(self.portal, 'portal_workflow')
        self.logout()
        state = portal_workflow.getInfoFor(fp, 'review_state')
        transitions = portal_workflow.getTransitionsFor(fp)
        transitions_list = [ x['id'] for x in transitions ]

        self.failUnlessEqual(state, wf_results['state'])
        self.failUnlessEqual(transitions_list, wf_results['transitions'])

    def test_get_workflow(self):
        """This tests for the results of the get_workflow logic and the
        format of the results."""
        # Setup the context variable.
        fp = self.portal['front-page']
        # First, setup the call results.
        resp = Response(FauxResponse())
        wf = Workflow(fp, '')
        self.login('test_user_1_')
        wf_data = wf.get_workflow()
        self.logout()
        resp.setBody(wf_data)
        wf_body = resp._body
        wf_resp, method = xmlrpclib.loads(wf_body)
        wf_results = wf_resp[0]
        # Now, get the results directly from the tool.
        portal_workflow = getToolByName(self.portal, 'portal_workflow')
        self.login('test_user_1_')
        state = portal_workflow.getInfoFor(fp, 'review_state')
        transitions = portal_workflow.getTransitionsFor(fp)
        self.logout()
        transitions_list = [ x['id'] for x in transitions ]

        self.failUnlessEqual(state, wf_results['state'])
        self.failUnlessEqual(transitions_list, wf_results['transitions'])

    def test_anonymous_set_workflow(self):
        # Setup the context variable.
        fp = self.portal['front-page']
        resp = Response(FauxResponse())
        # First, setup the call results.
        resp = Response(FauxResponse())
        wf = Workflow(fp, '')
        # Transition the workflow.
        self.logout() # Make sure we are logged out.
        try:
            wf_data = wf.set_workflow('retract')
        except WorkflowException:
            # The expected result.
            pass
        else:
            self.fail("An anonymous user was able to set the workflow.")

    def test_set_workflow(self):
        # Setup the context variable.
        fp = self.portal['front-page']
        resp = Response(FauxResponse())
        # First, setup the call results.
        resp = Response(FauxResponse())
        wf = Workflow(fp, '')
        # Transition the workflow.
        self.login('test_user_1_')
        wf_data = wf.set_workflow('retract')
        self.logout()
        resp.setBody(wf_data)
        wf_body = resp._body
        wf_resp, method = xmlrpclib.loads(wf_body)
        wf_results = wf_resp[0]
        # Test the result of the set_workflow call is None.
        self.failUnlessEqual(wf_results, None)
        # Verify the worflow has been changed.
        portal_workflow = getToolByName(self.portal, 'portal_workflow')
        state = portal_workflow.getInfoFor(fp, 'review_state')
        self.failUnlessEqual(state, 'private')

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestWorkflow))
    return suite

