#
# File: userfolder.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ""
__docformat__ = "plaintext"

"""Definition of the UserFolder content type. See userfolder.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from docpool.base.content.simplefolder import ISimpleFolder, SimpleFolder
from docpool.base.utils import _cutPaste, execute_under_special_role
from plone.supermodel import model
from Products.CMFCore.utils import getToolByName
from zope.interface import implementer


class IUserFolder(model.Schema, ISimpleFolder):
    """ """


@implementer(IUserFolder)
class UserFolder(SimpleFolder):
    """ """

    security = ClassSecurityInfo()

    def notifyMemberAreaCreated(self):
        """
        Move the member area to the proper location.
        """
        # print "notifyMemberAreaCreated"
        def moveFolder():
            # Determine the owner
            o = self.getOwner()
            if o:
                # Determine the corresponding ESD
                esd_uid = o.getProperty("dp")
                if esd_uid:
                    catalog = getToolByName(self, "portal_catalog")
                    result = catalog({"UID": esd_uid})
                    if len(result) == 1:
                        esd = result[0].getObject()
                        # Move me there
                        members = esd.content.Members
                        _cutPaste(self, members, unique=True)

        execute_under_special_role(self, "Manager", moveFolder)

    def myUserFolder(self):
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

    def getSimpleFolders(self, **kwargs):
        """ """
        args = {"portal_type": "SimpleFolder"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]
