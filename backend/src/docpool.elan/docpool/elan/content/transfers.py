from docpool.base.utils import _copyPaste
from docpool.elan.config import ELAN_APP
from docpool.elan.utils import getOpenScenarios
from plone import api
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

    for scenario in my_scenarios:
        if scen.hasObject(scenario):
            copy_id = scenario
            copy_event = scen[copy_id]
            if api.content.get_state(copy_event) == "private" and copy_event.Substitute:
                substitute = copy_event.Substitute.to_object
                if substitute.canBeAssigned():
                    copy_id = substitute.getId()
        else:
            orig_event = scen_source[scenario]
            copy_id = _copyPaste(orig_event, scen)
            copy_event = scen[copy_id]
            api.content.transition(copy_event, "retract")

        new_scenarios.append(copy_id)

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
