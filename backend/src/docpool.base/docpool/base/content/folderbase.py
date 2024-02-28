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

    def change_state(self, id, action, backToReferer=False, REQUEST=None):
        """ """
        if REQUEST:
            alsoProvides(REQUEST, IDisableCSRFProtection)
        if not action:
            return self.restrictedTraverse("@@view")()
        doc = None
        try:
            doc = self._getOb(id)
        except BaseException:
            pass
        if doc:
            wftool = getToolByName(self, "portal_workflow")
            try:
                wftool.doActionFor(doc, action)
                if (
                    str(action) == "publish"
                ):  # when publishing we also publish any document inside the current document
                    for subdoc in doc.getDPDocuments():
                        try:
                            wftool.doActionFor(subdoc, action)
                        except BaseException:
                            pass
            except BaseException:
                return self.restrictedTraverse("@@view")()
            if REQUEST:
                last_referer = REQUEST.get("HTTP_REFERER")
                portalMessage(self, _("The document state has been changed."), "info")
                if backToReferer and last_referer:
                    return REQUEST.RESPONSE.redirect(last_referer)
                else:
                    return self.restrictedTraverse("@@view")()

    def canBeDeleted(self, principal_deleted=False):
        """ """
        mtool = getToolByName(self, "portal_membership")
        if not mtool.checkPermission("Delete objects", self):
            return False
        else:
            return True
