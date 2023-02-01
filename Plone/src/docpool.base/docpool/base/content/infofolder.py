from docpool.base.content.folderbase import FolderBase
from docpool.base.content.folderbase import IFolderBase
from plone.supermodel import model
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import base_hasattr
from Products.CMFPlone.utils import log
from Products.CMFPlone.utils import log_exc
from zExceptions import BadRequest
from zope.interface import implementer


class IInfoFolder(model.Schema, IFolderBase):
    """ """


@implementer(IInfoFolder)
class InfoFolder(FolderBase):
    """ """

    def createActions(self):
        """ """
        if base_hasattr(self, "myGroupFolder"):
            log("Creating Private Info Folder")

            placeful_wf = getToolByName(self, "portal_placeful_workflow")
            try:
                self.manage_addProduct[
                    "CMFPlacefulWorkflow"
                ].manage_addWorkflowPolicyConfig()
            except BadRequest as e:
                log_exc(e)
            config = placeful_wf.getWorkflowPolicyConfig(self)
            placefulWfName = "dp-private-infofolder"
            config.setPolicyIn(policy=placefulWfName, update_security=False)
            config.setPolicyBelow(policy=placefulWfName, update_security=False)
            self.reindexObject()
            self.updateSecurity()
            self.reindexObjectSecurity()
