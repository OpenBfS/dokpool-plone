from docpool.base import DocpoolMessageFactory as _
from docpool.base.content.folderbase import FolderBase
from docpool.base.content.folderbase import IFolderBase
from docpool.base.utils import getAllowedDocumentTypes
from docpool.base.utils import portalMessage
from docpool.base.utils import queryForObjects
from plone import api
from plone.base.utils import safe_text
from plone.protect.interfaces import IDisableCSRFProtection
from plone.supermodel import model
from Products.CMFCore.utils import getToolByName
from zope import schema
from zope.interface import alsoProvides
from zope.interface import implementer


class ISimpleFolder(model.Schema, IFolderBase):
    """ """

    allowedDocTypes = schema.List(
        title=_(
            "label_simplefolder_alloweddoctypes",
            default="Document types allowed in this folder",
        ),
        description=_(
            "description_simplefolder_alloweddoctypes",
            default="Leave blank to enable all types configured for the group.",
        ),
        required=False,
        value_type=schema.Choice(source="docpool.base.vocabularies.GroupDocType"),
    )


@implementer(ISimpleFolder)
class SimpleFolder(FolderBase):
    """ """

    def customMenu(self, menu_items):
        """ """
        dts = getAllowedDocumentTypes(self)
        filter = False
        if self.allowedDocTypes:
            filter = True
        # Get active app
        app = ""
        user = api.user.get_current()
        if user:
            active_app = user.getProperty("apps")
            if active_app:
                app = active_app[0]
        res = []
        for menu_item in menu_items:
            if menu_item.get("id") == "DPDocument":
                for dt in dts:
                    if (
                        not dt.getObject().globalAllow
                    ):  # only generally allowed doctypes
                        continue
                    # Get behavior of menu_item
                    from docpool.base.localbehavior.localbehavior import (
                        ILocalBehaviorSupport,
                    )

                    item_behavior = ILocalBehaviorSupport(
                        dt.getObject()
                    ).local_behaviors

                    if not app in item_behavior:
                        continue
                    if not filter or dt.id in self.allowedDocTypes:
                        res.append(
                            {
                                "extra": {
                                    "separator": None,
                                    "id": dt.id,
                                    "class": "contenttype-%s" % dt.id,
                                },
                                "submenu": None,
                                "description": "",
                                "title": safe_text(dt.Title),
                                "action": "%s/++add++DPDocument?form.widgets.docType:list=%s"
                                % (self.absolute_url(), dt.id),
                                "selected": False,
                                "id": dt.id,
                                "icon": None,
                            }
                        )
            else:
                res.append(menu_item)
        return res

    def isPrincipalFolder(self):
        """ """
        return self.getPortalTypeName() in ["UserFolder", "GroupFolder"]

    def canBeDeleted(self, principal_deleted=False):
        """
        A folder can be deleted, if
        - it does not contain published Documents somewhere below AND
        - it is not a member or group root folder,
              unless principal_deleted = True
        """
        mtool = getToolByName(self, "portal_membership")
        if not mtool.checkPermission("Delete objects", self):
            return False
        if self.containsPublishedDocuments():
            return False
        if self.isPrincipalFolder():
            if principal_deleted:
                return True
            else:
                return False
        return True

    def containsPublishedDocuments(self):
        """ """
        return (
            len(
                queryForObjects(
                    self,
                    path="/".join(self.getPhysicalPath()),
                    portal_type="DPDocument",
                    review_state="published",
                )
            )
            > 0
        )

    def publish_doc(self, id, REQUEST=None):
        """ """
        if REQUEST:
            alsoProvides(REQUEST, IDisableCSRFProtection)
        doc = None
        try:
            doc = self._getOb(id)
        except BaseException:
            pass
        if doc:
            wftool = getToolByName(self, "portal_workflow")
            wftool.doActionFor(doc, "publish")
            if REQUEST:
                portalMessage(self, _("The document has been published."), "info")
                return self.restrictedTraverse("@@view")()
