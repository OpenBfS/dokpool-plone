from docpool.base import DocpoolMessageFactory as _
from docpool.base.content.contentbase import ContentBase
from docpool.base.content.contentbase import IContentBase
from docpool.base.utils import portalMessage
from plone.dexterity.content import Container
from plone.protect.interfaces import IDisableCSRFProtection
from Products.CMFCore.utils import getToolByName
from zope.interface import alsoProvides
from zope.interface import implementer


class IFolderBase(IContentBase):
    """ """


@implementer(IFolderBase)
class FolderBase(Container, ContentBase):
    """ """

    def myFolderBase(self):
        """ """
        return self

    def canBeDeleted(self, principal_deleted=False):
        """ """
        mtool = getToolByName(self, "portal_membership")
        if not mtool.checkPermission("Delete objects", self):
            return False
        else:
            return True
