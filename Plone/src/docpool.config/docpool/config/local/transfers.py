# -*- coding: utf-8 -*-
from Products.Archetypes.utils import shasattr
from docpool.config.utils import ID, TYPE, TITLE, CHILDREN, createPloneObjects
from zExceptions import BadRequest
from Products.CMFPlone.utils import log_exc
from Products.CMFCore.utils import getToolByName


def dpAdded(self):
    """
    """
    fresh = True
    if self.content.hasObject("Transfers"):
        fresh = False # It's a reinstall
    createTransferArea(self, fresh)
    if fresh:
        createTransfersGroups(self)
    setTransfersLocalRoles(self)

TRANSFER_AREA = [
    {TYPE: 'ELANTransfers', TITLE: u'Transfers', ID: 'Transfers', CHILDREN: []},
]

def setTransfersLocalRoles(self):
    """
    """
    prefix = self.prefix or self.getId()
    prefix = str(prefix)
    self.content.Transfers.manage_setLocalRoles("%s_Receivers" % prefix, ["Owner"])
    self.content.Transfers.manage_setLocalRoles("%s_Administrators" % prefix, ["Owner"])
    if shasattr(self, 'contentconfig', acquire=False):
        self.contentconfig.scen.manage_setLocalRoles("%s_Receivers" % prefix, ["ContentReceiver"])
    self.config.manage_setLocalRoles("%s_Receivers" % prefix, ["ContentReceiver"])
    self.content.Groups.manage_setLocalRoles("%s_Senders" % prefix, ["ContentSender"])

def createTransfersGroups(self):
    # - Receiving content from others
    # - Sending content to others

    prefix = self.prefix or self.getId()
    prefix = str(prefix)
    title = self.Title()
    gtool = getToolByName(self, 'portal_groups')
    props = {'allowedDocTypes': [], 'title': 'Content Receivers (%s)' % title,
             'description': 'Responsible for publishing content received from other ESDs.', 'dp': self.UID()}
    gtool.addGroup("%s_Receivers" % prefix,
                   properties=props)
    props = {'allowedDocTypes': [], 'title': 'Content Senders (%s)' % title,
             'description': 'Responsible for sending content to other ESDs - if allowed by them.', 'dp': self.UID()}
    gtool.addGroup("%s_Senders" % prefix,
                   properties=props)


def createTransferArea(self, fresh):
    """
    """
    createPloneObjects(self.content, TRANSFER_AREA, fresh)
    # Move to first position
    self.content.moveObject("Transfers", 0)
    placeful_wf = getToolByName(self, 'portal_placeful_workflow')
    try:
        self.content.Transfers.manage_addProduct['CMFPlacefulWorkflow'].manage_addWorkflowPolicyConfig()
    except BadRequest, e:
        # print type(e)
        log_exc(e)
    config = placeful_wf.getWorkflowPolicyConfig(self.content.Transfers)
    placefulWfName = 'elan-transfer'
    config.setPolicyIn(policy=placefulWfName, update_security=False)
    config.setPolicyBelow(policy=placefulWfName, update_security=False)

def dpRemoved(self):
    """
    @param self:
    @return:
    """
    return