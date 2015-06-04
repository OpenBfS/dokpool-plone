# -*- coding: utf-8 -*-

from elan.esd.content.elandocument import ELANDocument
from Products.CMFPlone.utils import log, log_exc

from plone.api import user
from Products.CMFCore.utils import getToolByName
from zExceptions import BadRequest

def createActions(self):
    ELANDocument.original_createActions(self)
#    print "CREATE"
    f = self.myELANFolder()
    r = user.get_roles(obj=f, inherit=True)
    if "Owner" in r:
        return
    if "Reviewer" in r:
        log("Setting Guest Workflow on Document " + self.getId())

        placeful_wf = getToolByName(self, 'portal_placeful_workflow')
        try:
            self.manage_addProduct['CMFPlacefulWorkflow'].manage_addWorkflowPolicyConfig()
        except BadRequest, e:
            log_exc(e)
        config = placeful_wf.getWorkflowPolicyConfig(self)
        placefulWfName = 'elan-guest-document'
        config.setPolicyIn(policy=placefulWfName, update_security=False)
        config.setPolicyBelow(policy=placefulWfName, update_security=False)
        self.reindexObject()
        self.reindexObjectSecurity()        


if not hasattr(ELANDocument, "original_createActions"):
    # print "patching GroupManager"
    ELANDocument.original_createActions = ELANDocument.createActions
    ELANDocument.createActions = createActions
