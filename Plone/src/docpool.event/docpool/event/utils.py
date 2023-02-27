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


def _get_selected_scenarios_for_user(user):
    selections_prop = user.getProperty("scenarios", [])
    return dict(line.strip().rsplit(':', 1) for line in selections_prop)


def getScenarioIdsForCurrentUser(self):
    scns = getScenariosForCurrentUser(self)
    # Historically, these used to be object ids, not uids. When switching to uids for
    # #5044, the scenarios attribute of documents and the corresponding catalog index
    # weren't touched, so we need to convert uids to ids for that use case.
    # Since not all call sites clearly operate on a specific docpool, we consider all
    # uids. This will conflate events from different docpools that happen to have the
    # same id (which likely wasn't a considered a use case at the time the attribute was
    # first created). Search results should thus remain the same as previously.
    return list(set(api.content.get(UID=uid).getId() for uid in scns))


def getScenariosForCurrentUser(self):
    """
    """
    mtool = getToolByName(self, "portal_membership")
    user = mtool.getAuthenticatedMember()
    sc = get_scenarios_for_user(self, user)
    return list(sc)


def get_scenarios_for_user(self, user):
    selections = _get_selected_scenarios_for_user(user)
    global_scenarios = get_global_scenario_selection()

    for scen, state in global_scenarios.items():
        if state in ('closed', 'removed'):
            selections.pop(scen, None)
        else:
            selections.setdefault(scen, state)

    scenarios = [
        scen for scen, selected in selections.items() if selected == 'selected'
    ]
    return scenarios


def setScenariosForCurrentUser(self, scenarios):
    """
    """
    user = api.user.get_current()
    set_scenarios_for_user(self, user, scenarios)


def set_scenarios_for_user(self, user, scenarios):
    selections = _get_selected_scenarios_for_user(user)
    global_scenarios = get_global_scenario_selection()

    selections.update(
        (scen, 'selected' if selected else 'deselected')
        for scen, selected in scenarios.items()
    )
    user.setMemberProperties(
        {
            "scenarios": [
                '{}:{}'.format(scen, selected)
                for scen, selected in selections.items()
                if global_scenarios.get(scen) != 'removed'
            ]
        }
    )


def get_global_scenario_selection():
    portal = api.portal.get()
    annotations = IAnnotations(portal)
    return annotations.setdefault(ANN_KEY_SCENARIO_SELECTION, PersistentMapping())
