from docpool.base.utils import getDocumentPoolSite
from persistent.list import PersistentList
from persistent.mapping import PersistentMapping
from plone import api
from Products.CMFCore.utils import getToolByName
from zope.annotation.interfaces import IAnnotations


ANN_KEY_SCENARIO_SELECTION = 'SCENARIO_SELECTION'


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
    scenarios = set(user.getProperty("scenarios", []))
    global_scenarios = get_global_scenario_selection()
    for scen, state in global_scenarios.items():
        if state == 'selected':
            scenarios.add(scen)
        elif state in ('closed', 'removed'):
            scenarios.discard(scen)
        else:
            assert False, '{0} is not a valid scenario selection state'.format(state)
    return list(scenarios)


def setScenariosForCurrentUser(self, scenarios):
    """
    """
    global_scenarios = get_global_scenario_selection()
    user = api.user.get_current()
    user.setMemberProperties(
        {
            "scenarios": [
                scen for scen in scenarios if global_scenarios.get(scen) != 'removed'
            ]
        }
    )


def get_global_scenario_selection():
    portal = api.portal.get()
    annotations = IAnnotations(portal)
    return annotations.setdefault(ANN_KEY_SCENARIO_SELECTION, PersistentMapping())
