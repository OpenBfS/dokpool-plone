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


def getScenariosForCurrentUser(self):
    """ """
    mtool = getToolByName(self, "portal_membership")
    user = mtool.getAuthenticatedMember()
    sc = get_scenarios_for_user(self, user)
    return list(sc)


def get_scenarios_for_user(self, user):
    selections_prop = user.getProperty("scenarios", [])
    global_scenarios = get_global_scenario_selection()

    selections = {}
    for line in selections_prop:
        line = line.strip()
        if line.endswith((":selected", ":deselected")):
            scen, selected = line.rsplit(":", 1)
            selections[scen] = selected
        else:
            # Avoid upgrade step for now. We used to store a list of selected scenarios.
            selections = dict.fromkeys(list(global_scenarios), False)
            selections.update(dict.fromkeys(selections_prop, True))
            break

    scenarios = [
        scen for scen, selected in selections.items() if selected == "selected"
    ]
    for scen, state in global_scenarios.items():
        selected = selections.get(scen)
        if (state == "selected" or selected == "selected") and not (
            state in ("closed", "removed") or selected == "deselected"
        ):
            scenarios.append(scen)
    # remove duplicates (events that are selected globally and by user)
    scenarios = list(set(scenarios))
    return scenarios


def setScenariosForCurrentUser(self, scenarios):
    """ """
    user = api.user.get_current()
    set_scenarios_for_user(self, user, scenarios)


def set_scenarios_for_user(self, user, scenarios):
    global_scenarios = get_global_scenario_selection()
    user.setMemberProperties(
        {
            "scenarios": [
                "{}:{}".format(scen, "selected" if scen in scenarios else "deselected")
                for scen in set(scenarios) | set(global_scenarios)
                if global_scenarios.get(scen) != "removed"
            ]
        }
    )


def get_global_scenario_selection():
    portal = api.portal.get()
    annotations = IAnnotations(portal)
    return annotations.setdefault(ANN_KEY_SCENARIO_SELECTION, PersistentMapping())
