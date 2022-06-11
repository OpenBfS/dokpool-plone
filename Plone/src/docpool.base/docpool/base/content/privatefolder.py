#
# File: privatefolder.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ""
__docformat__ = "plaintext"

"""Definition of the PrivateFolder content type. See privatefolder.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from docpool.base.content.simplefolder import ISimpleFolder, SimpleFolder
from plone.dexterity.content import Container
from plone.supermodel import model
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import log, log_exc
from zExceptions import BadRequest
from zope.interface import implementer


class IPrivateFolder(model.Schema, ISimpleFolder):
    """ """


@implementer(IPrivateFolder)
class PrivateFolder(Container, SimpleFolder):
    """ """

    security = ClassSecurityInfo()

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

    def myPrivateFolder(self):
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

    def getDPDocuments(self, **kwargs):
        """ """
        args = {"portal_type": "DPDocument"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getInfoDocuments(self, **kwargs):
        """ """
        args = {"portal_type": "InfoDocument"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getPrivateFolders(self, **kwargs):
        """ """
        args = {"portal_type": "PrivateFolder"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]
