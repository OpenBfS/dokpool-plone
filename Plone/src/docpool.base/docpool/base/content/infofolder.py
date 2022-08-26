#
# File: infofolder.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ""
__docformat__ = "plaintext"

"""Definition of the InfoFolder content type. See infofolder.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
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

    security = ClassSecurityInfo()

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

    def myInfoFolder(self):
        """ """
        return self

    def getFirstChild(self):
        """ """
        fc = self.getFolderContents()
        if len(fc) > 0:
            return fc[0].getObject()
        else:
            return None

    def getAllContentObjects(self):
        """ """
        return [obj.getObject() for obj in self.getFolderContents()]

    def getInfoDocuments(self, **kwargs):
        """ """
        args = {"portal_type": "InfoDocument"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getInfoFolders(self, **kwargs):
        """ """
        args = {"portal_type": "InfoFolder"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getInfoLinks(self, **kwargs):
        """ """
        args = {"portal_type": "InfoLink"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]
