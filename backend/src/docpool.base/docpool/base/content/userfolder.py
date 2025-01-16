from docpool.base.content.simplefolder import ISimpleFolder
from docpool.base.content.simplefolder import SimpleFolder
from docpool.base.utils import _cutPaste
from docpool.base.utils import execute_under_special_role
from docpool.doksys.config import DOKSYS_APP
from logging import getLogger
from plone import api
from plone.supermodel import model
from zope.interface import implementer


logger = getLogger(__name__)


class IUserFolder(model.Schema, ISimpleFolder):
    """ """


@implementer(IUserFolder)
class UserFolder(SimpleFolder):
    """ """

    APP = DOKSYS_APP

    def notifyMemberAreaCreated(self):
        """
        Move the member area to the proper location.
        This is called when a user logs in for the first time via loginUser and createMemberarea.
        """

        def moveFolder():
            # Determine the owner
            owner = self.getOwner()
            if owner:
                dp_uid = owner.getProperty("dp")
                if dp_uid:
                    old_url = self.absolute_url()
                    dp = api.content.get(UID=dp_uid)
                    members = dp.content.Members
                    new = _cutPaste(self, members, unique=True)
                    if new:
                        logger.info(
                            "Moved UserFolder %s to %s",
                            old_url,
                            new.absolute_url(),
                        )

        execute_under_special_role(self, "Manager", moveFolder)
