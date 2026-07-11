from docpool.base.utils import getDocumentPoolSite
from plone import api
from Products.CMFCore.utils import getToolByName


def getActiveScenarios(self):
    cat = getToolByName(self, "portal_catalog")
    esd = getDocumentPoolSite(self)
    res = cat(
        path="/".join(esd.getPhysicalPath()) + "/contentconfig",
        portal_type="DPEvent",
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
        portal_type="DPEvent",
        dp_type=["active", "inactive"],
        sort_on="created",
        sort_order="reverse",
    )
    return res


def get_scenario_for_current_user(context):
    user = api.user.get_current()
    value = user.getProperty("scenario", None)
    if api.content.find(UID=value, dp_type=["active", "inactive"]):
        return value
    # XXX We really want to fall back to some kind of default scenario. Any scenario is better than nothing
    # for the time being, though. For the sake of existing test setups, return "Normalfall" as a sensible
    # default.
    if brains := getOpenScenarios(context):
        for brain in brains:
            if brain.Title == "Normalfall":
                return brain.UID
        return brains[0].UID


def set_scenario_for_current_user(scenario):
    user = api.user.get_current()
    value = scenario if api.content.find(UID=scenario) else None
    if user.getProperty("scenarios", None) != value:
        user.setMemberProperties({"scenario": value})


def getAvailableCategories(self):
    esd = getDocumentPoolSite(self)
    path = "/".join(esd.getPhysicalPath()) + "/esd"
    brains = api.content.find(
        path=path,
        portal_type="ELANDocCollection",
        dp_type=["active"],
        sort_on="sortable_title",
    )
    return [i for i in brains if i.id not in ["recent", "overview"]]


def getCategoriesForCurrentUser():
    user = api.user.get_current()
    cs = user.getProperty("categories", None)
    if not cs:
        return []
    return list(cs)


def setCategoriesForCurrentUser(cats):
    """ """
    if isinstance(cats, str):
        cats = [cats]
    user = api.user.get_current()
    if sorted(user.getProperty("categories", [])) != sorted(cats):
        user.setMemberProperties({"categories": cats})
