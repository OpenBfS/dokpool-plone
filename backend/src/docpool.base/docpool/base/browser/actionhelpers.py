from docpool.base.content.dpdocument import IDPDocument
from plone import api
from Products.Five.browser import BrowserView

import logging


log = logging.getLogger(__name__)


class ActionHelpers(BrowserView):
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
        wf_tool = api.portal.get_tool("portal_workflow")
        workflow = wf_tool.getWorkflowsFor(doc)[0]
        rei_wfs = ["rei_review_workflow_alternative", "rei_review_workflow_standard"]
        if workflow.id in rei_wfs:
            return True
        return False
