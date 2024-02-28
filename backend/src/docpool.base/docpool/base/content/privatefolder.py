from docpool.base.content.simplefolder import ISimpleFolder
from docpool.base.content.simplefolder import SimpleFolder
from plone.supermodel import model
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import log
from Products.CMFPlone.utils import log_exc
from zExceptions import BadRequest
from zope.interface import implementer


class IPrivateFolder(model.Schema, ISimpleFolder):
    """ """


@implementer(IPrivateFolder)
class PrivateFolder(SimpleFolder):
    """ """

    def createActions(self):
        """ """
        log("Creating Private Folder")

        placeful_wf = getToolByName(self, "portal_placeful_workflow")
        try:
            self.manage_addProduct[
                "CMFPlacefulWorkflow"
            ].manage_addWorkflowPolicyConfig()
        except BadRequest as e:
            log_exc(e)
        config = placeful_wf.getWorkflowPolicyConfig(self)
        placefulWfName = "dp-private-folder"
        config.setPolicyIn(policy=placefulWfName, update_security=False)
        config.setPolicyBelow(policy=placefulWfName, update_security=False)
        self.reindexObject()
        self.updateSecurity()
        self.reindexObjectSecurity()
