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
    scen = copy.myDocumentPool().contentconfig.scen
    copy_events = []

    for orig_brain in api.content.find(UID=my_scenarios):
        copy_id = orig_brain.getId
        if scen.hasObject(copy_id):
            copy_event = scen[copy_id]
            if api.content.get_state(copy_event) == "private" and copy_event.Substitute:
                substitute = copy_event.Substitute.to_object
                if substitute.canBeAssigned():
                    copy_event = substitute
        else:
            orig_event = orig_brain.getObject()
            copy_id = _copyPaste(orig_event, scen)
            copy_event = scen[copy_id]
            api.content.transition(copy_event, "retract")

        copy_events.append(copy_event)

    try:
        copy.doc_extension(ELAN_APP).scenarios = [e.UID() for e in copy_events]
    except Exception as e:
        log_exc(e)

    return [e.getId() for e in copy_events]


def knowsScen(transfer_folder, scen_id):
    """
    Do I know this scenario?
    """
    scens = getOpenScenarios(transfer_folder)
    scen_ids = [scen.getId for scen in scens]
    return scen_id in scen_ids
