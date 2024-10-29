from docpool.base.utils import getDocumentPoolSite
from persistent.mapping import PersistentMapping
from plone import api
from Products.CMFCore.utils import getToolByName
from zope.annotation.interfaces import IAnnotations


ANN_KEY_SCENARIO_SELECTION = "SCENARIO_SELECTION"


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


def getScenariosForCurrentUser():
    """ """
    mtool = api.portal.get_tool("portal_membership")
    user = mtool.getAuthenticatedMember()
    sc = get_scenarios_for_user(user)
    return list(sc)


def get_scenarios_for_user(user):
    selections_prop = user.getProperty("scenarios", [])
    global_scenarios = get_global_scenario_selection()

    selections = dict(line.strip().rsplit(":", 1) for line in selections_prop)

    for scen, state in global_scenarios.items():
        if state in ("closed", "removed"):
            selections.pop(scen, None)
        else:
            selections.setdefault(scen, state)

    scenarios = [
        scen for scen, selected in selections.items() if selected == "selected"
    ]
    return scenarios


def setScenariosForCurrentUser(scenarios):
    """ """
    user = api.user.get_current()
    set_scenarios_for_user(user, scenarios)


def set_scenarios_for_user(user, scenarios):
    global_scenarios = get_global_scenario_selection()
    user.setMemberProperties(
        {
            "scenarios": [
                "{}:{}".format(scen, "selected" if selected else "deselected")
                for scen, selected in scenarios.items()
                if global_scenarios.get(scen) != "removed"
            ]
        }
    )


def get_global_scenario_selection():
    portal = api.portal.get()
    annotations = IAnnotations(portal)
    return annotations.setdefault(ANN_KEY_SCENARIO_SELECTION, PersistentMapping())


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


def getCategoriesForCurrentUser(self):
    user = api.user.get_current()
    cs = user.getProperty("categories", None)
    if not cs:
        return []
    return list(cs)


def setCategoriesForCurrentUser(self, cats):
    """ """
    if isinstance(cats, str):
        cats = [cats]
    user = api.user.get_current()
    user.setMemberProperties({"categories": cats})
