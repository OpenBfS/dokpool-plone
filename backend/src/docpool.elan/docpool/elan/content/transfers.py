from docpool.base import DocpoolMessageFactory as _
from docpool.base.behaviors.transferable import IAppSpecificTransfer
from docpool.base.content.dpdocument import IDPDocument
from docpool.base.content.dptransferfolder import IDPTransferFolder
from docpool.base.utils import _copyPaste
from docpool.elan.behaviors.elandocument import IELANDocument
from docpool.elan.config import ELAN_APP
from docpool.elan.utils import getOpenScenarios
from plone import api
from Products.CMFPlone.utils import log_exc
from zope.component import adapter
from zope.interface import implementer
from zope.interface import named


@adapter(IDPDocument, IDPTransferFolder)
@implementer(IAppSpecificTransfer)
@named(ELAN_APP)
class ELANSpecificTransfer:
    def __init__(self, original, transfer_folder):
        self.original = original
        self.transfer_folder = transfer_folder
        self.elanobj = IELANDocument(self.original, None)

    def assert_allowed(self):
        # Is my Scenario known, are unknown Scenarios accepted?
        scen_ok = self.transfer_folder.unknownScenDefault != "block"
        if not scen_ok:
            # check my precise Scenario
            # TODO The following is inefficient in that it creates a list of
            # full objects, but it effectively filters elanobj.scenarios for
            # those that actually exist in the catalog. Is this necessary?
            # FIXME: The following logic appears to be broken, see #5723.
            scens = self.elanobj.myScenarioObjects()
            if scens:
                scen_id = scens[0].getId()
                if not any(scen.getId == scen_id for scen in getOpenScenarios(self.transfer_folder)):
                    raise ValueError(_("Unknown scenario not accepted."))
            else:
                raise ValueError(_("Document has no scenario."))

    def sender_log_entry(self):
        scenario_ids = ", ".join(b.getId for b in api.content.find(UID=self.elanobj.scenarios))
        return dict(scenario_ids=scenario_ids)

    def __call__(self, copy):
        self.copy_scenario_ids = ensureScenariosInTarget(self.original, copy)

    def receiver_log_entry(self):
        return dict(scenario_ids=", ".join(self.copy_scenario_ids))


def ensureScenariosInTarget(original, copy):
    """Handle scenario assignments on document transfer.

    For each scenario assigned to the original, try to identify a scenario at the target
    ESD, matching by object id. Copy unmatched scenarios to target ESD.

    According to #5872, make sure copied scenarios are in published state. For each
    existing equivalent scenario in the target that is in private state, if it defines
    a published substitute scenario, replace it with that.

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
            if api.content.get_state(copy_event) == "private":
                api.content.transition(copy_event, "publish")

        copy_events.append(copy_event)

    try:
        copy.doc_extension(ELAN_APP).scenarios = [e.UID() for e in copy_events]
    except Exception as e:
        log_exc(e)

    return [e.getId() for e in copy_events]
