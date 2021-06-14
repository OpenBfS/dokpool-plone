from docpool.base.utils import getDocumentPoolSite
from plone import api
from Products.CMFCore.utils import getToolByName


def getActiveScenarios(self):
    cat = getToolByName(self, "portal_catalog")
    esd = getDocumentPoolSite(self)
    res = cat(
        path="/".join(esd.getPhysicalPath()) + "/contentconfig",
        portal_type='DPEvent',
        dp_type="active",
        sort_on="modified",
        sort_order="reverse",
    )
    return res


def getOpenScenarios(self):
    cat = getToolByName(self, "portal_catalog")
    esd = getDocumentPoolSite(self)
    res = cat(
        path="/".join(esd.getPhysicalPath()) + "/contentconfig",
        portal_type='DPEvent',
        dp_type=["active", "inactive"],
        sort_on="created",
        sort_order="reverse",
    )
    return res


def getScenariosForCurrentUser(self):
    """
    """
    mtool = getToolByName(self, "portal_membership")
    user = mtool.getAuthenticatedMember()
    sc = get_scenarios_for_user(self, user)
    return list(sc)


def get_scenarios_for_user(self, user):
    scenarios = user.getProperty("scenarios", [])
    return scenarios


def setScenariosForCurrentUser(self, scenarios):
    """
    """
    user = api.user.get_current()
    user.setMemberProperties({"scenarios": scenarios})
