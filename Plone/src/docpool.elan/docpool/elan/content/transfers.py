from docpool.base.utils import _copyPaste
from docpool.elan.config import ELAN_APP
from docpool.event.utils import getOpenScenarios
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import log_exc


def ensureScenariosInTarget(original, copy):
    """If original's scenarios are unknown in the target ESD, copy them to the target.

    Set them to private state. For those with an equivalent scenario in the target that
    is in private state, check if it defines a published substitute scenario. If it
    does, change the scenario for the copy to that one.

    """
    my_scenarios = original.doc_extension(ELAN_APP).scenarios
    scen_source = original.myDocumentPool().contentconfig.scen
    scen = copy.myDocumentPool().contentconfig.scen
    new_scenarios = []
    wftool = getToolByName(original, "portal_workflow")
    for scenario in my_scenarios:
        if scen.hasObject(scenario):
            s = scen._getOb(scenario)
            if wftool.getInfoFor(s, "review_state") == "private":
                sscen = s.Substitute and s.Substitute.to_object or None
                if sscen and sscen.canBeAssigned():
                    substitute = sscen.getId()
                    new_scenarios.append(substitute)
                else:
                    new_scenarios.append(scenario)
            else:
                new_scenarios.append(scenario)
        else:
            s = scen_source._getOb(scenario)
            id = _copyPaste(s, scen)
            new_scen = scen._getOb(id)
            wftool = getToolByName(original, "portal_workflow")
            wftool.doActionFor(new_scen, "retract")
            new_scenarios.append(id)
    try:
        copy.doc_extension(ELAN_APP).scenarios = new_scenarios
    except Exception as e:
        log_exc(e)
    copy.reindexObject()


def knowsScen(transfer_folder, scen_id):
    """
    Do I know this scenario?
    """
    scens = getOpenScenarios(transfer_folder)
    scen_ids = [scen.getId for scen in scens]
    return scen_id in scen_ids
