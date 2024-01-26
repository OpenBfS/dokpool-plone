from docpool.base.content.simplefolder import ISimpleFolder
from docpool.base.content.simplefolder import SimpleFolder
from docpool.base.utils import _cutPaste
from docpool.base.utils import execute_under_special_role
from docpool.doksys.config import DOKSYS_APP
from plone.supermodel import model
from Products.CMFCore.utils import getToolByName
from zope.interface import implementer


class IUserFolder(model.Schema, ISimpleFolder):
    """ """


@implementer(IUserFolder)
class UserFolder(SimpleFolder):
    """ """

    APP = DOKSYS_APP

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
