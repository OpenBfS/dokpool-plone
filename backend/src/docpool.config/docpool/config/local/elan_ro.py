from ..utils import set_local_roles
from datetime import datetime
from docpool.base.content.documentpool import APPLICATIONS_KEY
from docpool.config import _
from docpool.config.general.elan import connectTypesAndCategories
from docpool.config.local.base import CONTENT_AREA
from docpool.config.utils import CHILDREN
from docpool.config.utils import createPloneObjects
from docpool.config.utils import ID
from docpool.config.utils import TITLE
from docpool.config.utils import TYPE
from docpool.elan.config import ELAN_APP
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import log_exc
from zExceptions import BadRequest
from zope.annotation.interfaces import IAnnotations

import transaction


# ELAN specific structures


def dpAdded(self):
    """ """
    annotations = IAnnotations(self)
    fresh = ELAN_APP not in annotations[APPLICATIONS_KEY]
    if fresh:
        annotations[APPLICATIONS_KEY].append(ELAN_APP)

    copyCurrentSituation(self, fresh)
    transaction.commit()
    createBasicPortalStructure(self, fresh)
    transaction.commit()
    createContentConfig(self, fresh)
    transaction.commit()
    if fresh:
        self.esd.correctAllDocTypes()
        transaction.commit()
        connectTypesAndCategories(self)

        placeful_wf = getToolByName(self, "portal_placeful_workflow")
        try:
            self.archive.manage_addProduct["CMFPlacefulWorkflow"].manage_addWorkflowPolicyConfig()
        except BadRequest as e:
            # print type(e)
            log_exc(e)
        config = placeful_wf.getWorkflowPolicyConfig(self.archive)
        placefulWfName = "elan-archive"
        config.setPolicyIn(policy=placefulWfName, update_security=False)
        config.setPolicyBelow(policy=placefulWfName, update_security=False)
        createELANUsers(self)
        createELANGroups(self)
        setELANLocalRoles(self)
        self.reindexAll()


BASICSTRUCTURE = [
    {
        TYPE: "ELANArchives",
        TITLE: "Archive",
        ID: "archive",
        CHILDREN: [],
        "local_behaviors": ["elan"],
    }
]

ARCHIVESTRUCTURE = [
    {
        TYPE: "ELANCurrentSituation",
        TITLE: "Electronic Situation Display",
        ID: "esd",
        CHILDREN: [],
    },
    CONTENT_AREA,
]

SPECIAL_PAGES = [
    {TYPE: "Text", TITLE: "Hilfe", ID: "help", CHILDREN: []},
]

ADMINSTRUCTURE = [
    {
        TYPE: "ELANContentConfig",
        TITLE: "Content Configuration",
        ID: "contentconfig",
        CHILDREN: [
            {
                TYPE: "DPEvents",
                TITLE: "Scenarios",
                ID: "scen",
                CHILDREN: [
                    {
                        TYPE: "DPEvent",
                        TITLE: "Routine mode",
                        ID: "routinemode",
                        "Status": "active",
                        "TimeOfEvent": datetime.now(),
                        "EventType": "Emergency",
                        "OperationMode": "routine",
                        "AlertingStatus": "none",
                        CHILDREN: [],
                    }
                ],
            },
            {TYPE: "Text", TITLE: "Ticker", ID: "ticker", CHILDREN: []},
            {TYPE: "Text", TITLE: "Hilfe", ID: "help", CHILDREN: []},
            {
                TYPE: "DashboardsConfig",
                TITLE: "Dashboard Configuration",
                ID: "dbconfig",
                CHILDREN: [],
            },
        ],
    }
] + SPECIAL_PAGES


def createBasicPortalStructure(plonesite, fresh):
    """ """
    createPloneObjects(plonesite, BASICSTRUCTURE, fresh)


def createContentConfig(plonesite, fresh):
    """ """
    createPloneObjects(plonesite, ADMINSTRUCTURE, fresh)


def createELANUsers(self):
    # Set type for user folders
    mtool = getToolByName(self, "portal_membership")
    prefix = self.prefix or self.getId()
    prefix = str(prefix)
    title = self.Title()
    mtool.addMember("%s_elanadmin" % prefix, "ELAN Administrator (%s)" % title, ["Member"], [])
    elanadmin = mtool.getMemberById("%s_elanadmin" % prefix)
    elanadmin.setMemberProperties({
        "fullname": "ELAN Administrator (%s)" % title,
        "dp": self.UID(),
    })
    elanadmin.setSecurityProfile(password="admin")
    mtool.addMember("%s_contentadmin" % prefix, "Content Admin (%s)" % title, ["Member"], [])
    contentadmin = mtool.getMemberById("%s_contentadmin" % prefix)
    contentadmin.setMemberProperties({
        "fullname": "Content Admin (%s)" % title,
        "dp": self.UID(),
    })
    contentadmin.setSecurityProfile(password="admin")


def setELANLocalRoles(self):
    """
    Normal local members: Reader
    Administrators: Site Administrator
    ContentAdministrators: Reviewer
    Receivers: Owner, Editor
    Senders: Contributor
    """
    contentadmin = "{0}_ContentAdministrators"
    set_local_roles(self, self, "{0}_SituationReportAdmins", ["SituationReportAdmin"])
    set_local_roles(self, self.contentconfig, contentadmin, ["ContentAdmin"])
    for pagedef in SPECIAL_PAGES:
        name = pagedef[ID]
        set_local_roles(self, self[name], contentadmin, ["ContentAdmin"])
    set_local_roles(self, self.archive, contentadmin, ["DocPoolAdmin"])
    set_local_roles(self, self.content.Groups, contentadmin, ["Site Administrator"])
    set_local_roles(self, self.esd, contentadmin, ["ContentAdmin"])
    set_local_roles(self, self, "{0}_ELANUsers", ["ELANUser"])
    set_local_roles(self, self.config, contentadmin, ["Owner"])


def createELANGroups(self):
    # We need local groups for
    # - General access to the ESD
    # - Administration
    # - Content Administration
    # - Receiving content from others
    # - Sending content to others

    prefix = self.prefix or self.getId()
    prefix = str(prefix)
    title = self.Title()
    gtool = getToolByName(self, "portal_groups")
    gtool.addPrincipalToGroup("%s_elanadmin" % prefix, "%s_Members" % prefix)
    gtool.addPrincipalToGroup("%s_contentadmin" % prefix, "%s_Members" % prefix)
    gtool.addPrincipalToGroup("%s_elanadmin" % prefix, "%s_Administrators" % prefix)
    # Content administrator group
    props = {
        "allowedDocTypes": [],
        "title": "Content Administrators (%s)" % title,
        "description": "Responsible for the definition of scenarios, ticker texts and additional content.",
        "dp": self.UID(),
    }
    gtool.addGroup("%s_ContentAdministrators" % prefix, properties=props)
    gtool.addPrincipalToGroup("%s_contentadmin" % prefix, "%s_ContentAdministrators" % prefix)
    # Group for ELAN application rights
    props = {
        "allowedDocTypes": [],
        "title": "ELAN Users (%s)" % title,
        "description": "Users with access to ELAN functions.",
        "dp": self.UID(),
    }
    gtool.addGroup("%s_ELANUsers" % prefix, properties=props)
    gtool.addPrincipalToGroup("%s_elanadmin" % prefix, "%s_ELANUsers" % prefix)
    gtool.addPrincipalToGroup("%s_contentadmin" % prefix, "%s_ELANUsers" % prefix)
    gtool.addPrincipalToGroup("%s_dpadmin" % prefix, "%s_ELANUsers" % prefix)
    # Group for Situation Report users
    props = {
        "allowedDocTypes": [],
        "title": "Situation Report Admins/Lagebild (%s)" % title,
        "description": "Users who can manage situation reports.",
        "dp": self.UID(),
    }
    gtool.addGroup("%s_SituationReportAdmins" % prefix, properties=props)
    gtool.addPrincipalToGroup("%s_contentadmin" % prefix, "%s_SituationReportAdmins" % prefix)
    gtool.addPrincipalToGroup("%s_dpadmin" % prefix, "%s_SituationReportAdmins" % prefix)
    gtool.addPrincipalToGroup("%s_elanadmin" % prefix, "%s_SituationReportAdmins" % prefix)


def copyCurrentSituation(self, fresh):
    """ """
    if not fresh:
        return
    esd = self.esd
    from docpool.base.utils import _copyPaste

    _copyPaste(esd, self, safe=False)
    self.esd.setTitle(_("Situation Display"))
    self.esd.reindexObject()
    # make sure the current situation is first
    self.moveObject("esd", 0)


def dpRemoved(self):
    """
    @param self:
    @return:
    """
    return
