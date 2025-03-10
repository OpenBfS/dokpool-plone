from AccessControl import ClassSecurityInfo
from docpool.base import DocpoolMessageFactory as _
from docpool.base.content.simplefolder import ISimpleFolder
from docpool.base.content.simplefolder import SimpleFolder
from docpool.base.utils import getAllowedDocumentTypesForGroup
from plone.api import user
from plone.base.utils import safe_text
from plone.supermodel import model
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import log
from Products.CMFPlone.utils import log_exc
from zExceptions import BadRequest
from zope import schema
from zope.interface import implementer


class ICollaborationFolder(model.Schema, ISimpleFolder):
    """ """

    allowedPartnerDocTypes = schema.List(
        title=_(
            "label_collaborationfolder_allowedpartnerdoctypes",
            default="Document types allowed for the guest group(s)",
        ),
        description=_(
            "description_collaborationfolder_allowedpartnerdoctypes", default=""
        ),
        required=True,
        value_type=schema.Choice(source="docpool.base.vocabularies.GroupDocType"),
    )


@implementer(ICollaborationFolder)
class CollaborationFolder(SimpleFolder):
    """ """

    security = ClassSecurityInfo()

    def createActions(self):
        """ """
        log("Creating Collaboration Folder")

        placeful_wf = getToolByName(self, "portal_placeful_workflow")
        try:
            self.manage_addProduct[
                "CMFPlacefulWorkflow"
            ].manage_addWorkflowPolicyConfig()
        except BadRequest as e:
            log_exc(e)
        config = placeful_wf.getWorkflowPolicyConfig(self)
        placefulWfName = "dp-collaboration-folder"
        config.setPolicyIn(policy=placefulWfName, update_security=False)
        config.setPolicyBelow(policy=placefulWfName, update_security=False)
        self.reindexObject()
        self.updateSecurity()
        self.reindexObjectSecurity()

    def customMenu(self, menu_items):
        """ """
        # print user.get_roles(obj=self)
        if "Reviewer" not in user.get_roles(obj=self):
            return SimpleFolder.customMenu(self, menu_items)
        else:
            # print "Reviewer"
            dts = getAllowedDocumentTypesForGroup(self)
            filter = False
            if self.allowedPartnerDocTypes:
                # print self.allowedPartnerDocTypes
                filter = True
            res = []
            for menu_item in menu_items:
                if menu_item.get("id") == "DPDocument":
                    for dt in dts:
                        # print dt.id
                        if (
                            not dt.getObject().globalAllow
                        ):  # only generally allowed doctypes
                            continue
                        if not filter or dt.id in self.allowedPartnerDocTypes:
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

    def myCollaborationFolder(self):
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
