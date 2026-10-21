from ..utils import set_local_roles
from docpool.base.content.documentpool import APPLICATIONS_KEY
from docpool.base.utils import RARELY_USED_TYPES
from docpool.config.local.base import CONTENT_AREA
from docpool.config.utils import CHILDREN
from docpool.config.utils import createPloneObjects
from docpool.config.utils import ID
from docpool.config.utils import TITLE
from docpool.config.utils import TYPE
from docpool.elan.config import ELAN_APP
from docpool.elan.content.dpevents import global_events_by_uid
from plone import api
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import log_exc
from zExceptions import BadRequest
from zope.annotation.interfaces import IAnnotations

import transaction


# ELAN specific structures

RARELY_USED_TYPES.add("SRFolder")


def dpAdded(self):
    """ """
    annotations = IAnnotations(self)
    fresh = ELAN_APP not in annotations[APPLICATIONS_KEY]
    if fresh:
        annotations[APPLICATIONS_KEY].append(ELAN_APP)

    transaction.commit()
    createBasicPortalStructure(self, fresh)
    transaction.commit()
    createContentConfig(self, fresh)
    transaction.commit()
    subscribe_events(self)
    transaction.commit()
    if fresh:
        transaction.commit()

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
    CONTENT_AREA,
]

SPECIAL_PAGES = [
    {TYPE: "Text", TITLE: "Hilfe", ID: "help", CHILDREN: []},
]

ADMINSTRUCTURE = [
    {
        TYPE: "ELANContentConfig",
        TITLE: "Konfiguration Inhalte",
        ID: "contentconfig",
        CHILDREN: [
            {
                TYPE: "DPEvents",
                TITLE: "Ereignisse",
                ID: "scen",
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


def subscribe_events(dp):
    dp["contentconfig"]["scen"].subscribed_events.extend(global_events_by_uid())


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
    set_local_roles(self, self, "{0}_ELANUsers", ["ELANUser"])
    set_local_roles(self, self.config, contentadmin, ["Owner"])
    set_local_roles(self, api.portal.get().contentconfig, "{0}_ELANUsers", ["Reader"])


def createELANGroups(self):
    # We need local groups for
    # - General access to the ESD
    # - Administration
    # - Content Administration
    # - Receiving content from others
    # - Sending content to others

    prefix = self.prefix or self.getId()
    title = self.Title()
    gtool = getToolByName(self, "portal_groups")

    # Content administrator group
    props = {
        "allowedDocTypes": [],
        "title": "Content Administrators (%s)" % title,
        "description": "Responsible for the definition of scenarios and additional content.",
        "dp": self.UID(),
    }
    gtool.addGroup("%s_ContentAdministrators" % prefix, properties=props)
    # Group for ELAN application rights
    props = {
        "allowedDocTypes": [],
        "title": "ELAN Users (%s)" % title,
        "description": "Users with access to ELAN functions.",
        "dp": self.UID(),
    }
    gtool.addGroup("%s_ELANUsers" % prefix, properties=props)
    # Group for Situation Report users
    props = {
        "allowedDocTypes": [],
        "title": "Situation Report Admins/Lagebild (%s)" % title,
        "description": "Users who can manage situation reports.",
        "dp": self.UID(),
    }
    gtool.addGroup("%s_SituationReportAdmins" % prefix, properties=props)

    # Add 10 groups that can manage event journals
    for index in range(1, 6):
        props = {
            "allowedDocTypes": [],
            "title": f"Journal {index} Editors ({title})",
            "description": f"Users who can edit journal{index} in {title}.",
            "dp": self.UID(),
        }
        gtool.addGroup(f"{prefix}_Journal{index}_Editors", properties=props)

    for index in range(1, 6):
        props = {
            "allowedDocTypes": [],
            "title": f"Journal {index} Reader ({title})",
            "description": f"Users who can view journal{index} in {title}.",
            "dp": self.UID(),
        }
        gtool.addGroup(f"{prefix}_Journal{index}_Readers", properties=props)


def dpRemoved(self):
    """
    @param self:
    @return:
    """
    return
