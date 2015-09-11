try:
    from zope.component.hooks import getSite
except ImportError:
    from zope.component.hooks import getSite
from zope.interface import implements

from interfaces import IWorkflow
from wsapi import WSAPI
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides

class Workflow(WSAPI):
    implements(IWorkflow)

    def get_workflow(self, path=''):
        """
        @param path - string to the path of the wanted object
        """
        alsoProvides(self.context.REQUEST, IDisableCSRFProtection)
        
        obj = self.builder(self.context, path)
        portal_workflow = getSite().portal_workflow
        results = {}

        self.logger.info("- get_workflow - Getting workflow state for %s." % (obj))

        results['state'] = current_state = portal_workflow.getInfoFor(obj, 'review_state')

        results['transitions'] = [ x['id'] for x in portal_workflow.getTransitionsFor(obj) ]
        return results

    def set_workflow(self, transition, path=''):
        """
        @param transition - string representing the workflow transition action
        @param path - string to the path of the wanted object
        """
        alsoProvides(self.context.REQUEST, IDisableCSRFProtection)
        obj = self.builder(self.context, path)
        portal_workflow = getSite().portal_workflow

        self.logger.info("- set_workflow - Transitioning (%s) workflow state for %s." % (transition, obj))

        # action/transition verification/validation is done in doActionFor
        portal_workflow.doActionFor(obj, transition)
        return
