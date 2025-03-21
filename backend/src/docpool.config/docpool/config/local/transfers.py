from docpool.base.content.documentpool import APPLICATIONS_KEY
from docpool.config.utils import CHILDREN
from docpool.config.utils import createPloneObjects
from docpool.config.utils import ID
from docpool.config.utils import TITLE
from docpool.config.utils import TYPE
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import base_hasattr
from Products.CMFPlone.utils import log
from zExceptions import BadRequest
from zope.annotation.interfaces import IAnnotations


def dpAdded(self):
    """ """
    annotations = IAnnotations(self)
    # prevent circular import
    from docpool.base.config import TRANSFERS_APP

    fresh = TRANSFERS_APP not in annotations[APPLICATIONS_KEY]
    if fresh:
        annotations[APPLICATIONS_KEY].append(TRANSFERS_APP)

    createTransferArea(self, fresh)
    if fresh:
        createTransfersGroups(self)
    setTransfersLocalRoles(self)


TRANSFER_AREA = [
    {TYPE: "DPTransfersArea", TITLE: "Transfers", ID: "Transfers", CHILDREN: []}
]


def setTransfersLocalRoles(self):
    """ """
    prefix = self.prefix or self.getId()
    prefix = str(prefix)
    self.content.Transfers.manage_setLocalRoles("%s_Receivers" % prefix, ["Owner"])
    self.content.Transfers.manage_setLocalRoles("%s_Administrators" % prefix, ["Owner"])
    if base_hasattr(self, "contentconfig"):
        self.contentconfig.scen.manage_setLocalRoles(
            "%s_Receivers" % prefix, ["ContentReceiver"]
        )
    self.config.manage_setLocalRoles("%s_Receivers" % prefix, ["ContentReceiver"])
    self.content.Groups.manage_setLocalRoles("%s_Senders" % prefix, ["ContentSender"])


def createTransfersGroups(self):
    # - Receiving content from others
    # - Sending content to others

    prefix = self.prefix or self.getId()
    prefix = str(prefix)
    title = self.Title()
    gtool = getToolByName(self, "portal_groups")
    # Receivers
    props = {
        "allowedDocTypes": [],
        "title": "Content Receivers (%s)" % title,
        "description": "Responsible for publishing content received from other ESDs.",
        "dp": self.UID(),
    }
    gtool.addGroup("%s_Receivers" % prefix, properties=props)
    # Senders
    props = {
        "allowedDocTypes": [],
        "title": "Content Senders (%s)" % title,
        "description": "Responsible for sending content to other ESDs - if allowed by them.",
        "dp": self.UID(),
    }
    gtool.addGroup("%s_Senders" % prefix, properties=props)


def createTransferArea(self, fresh):
    """ """
    createPloneObjects(self.content, TRANSFER_AREA, fresh)
    # Move to first position
    self.content.moveObject("Transfers", 0)
    placeful_wf = getToolByName(self, "portal_placeful_workflow")
    try:
        self.content.Transfers.manage_addProduct[
            "CMFPlacefulWorkflow"
        ].manage_addWorkflowPolicyConfig()
    except BadRequest as e:
        # print type(e)
        log(e)
    config = placeful_wf.getWorkflowPolicyConfig(self.content.Transfers)
    placefulWfName = "elan-transfer"
    config.setPolicyIn(policy=placefulWfName, update_security=False)
    config.setPolicyBelow(policy=placefulWfName, update_security=False)


def dpRemoved(self):
    """
    @param self:
    @return:
    """
    return
