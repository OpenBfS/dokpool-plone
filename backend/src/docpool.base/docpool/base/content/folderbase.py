from docpool.base.content.contentbase import ContentBase
from docpool.base.content.contentbase import IContentBase
from plone.dexterity.content import Container
from Products.CMFCore.utils import getToolByName
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
