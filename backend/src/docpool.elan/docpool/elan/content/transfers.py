from docpool.base.behaviors.transferable import IAppSpecificTransfer
from docpool.base.content.dpdocument import IDPDocument
from docpool.base.content.dptransferfolder import IDPTransferFolder
from docpool.base.utils import _copyPaste
from docpool.elan.behaviors.elandocument import IELANDocument
from docpool.elan.config import ELAN_APP
from plone import api
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
        self.have_elan = ELAN_APP in self.transfer_folder.myDocumentPool().supportedApps
        self.copy_scenario = None

    def assert_allowed(self):
        return

    def sender_log_entry(self):
        scenario_id = (
            scen.id if (uid := self.elanobj.scenario) and (scen := api.content.get(UID=uid)) else None
        )
        return dict(scenario_id=scenario_id)

    def __call__(self, copy):
        if not self.have_elan:
            try:
                del copy.aq_base.scenario
            except AttributeError:
                pass
            return

        (elan_copy := IELANDocument(copy)).scenario = None
        if not self.elanobj.scenario:
            return

        self.copy_scenario = ensureScenarioInTarget(self.elanobj.scenario, copy.myDocumentPool())
        if self.copy_scenario:
            elan_copy.scenario = self.copy_scenario.UID()

    def receiver_log_entry(self):
        if not self.have_elan or self.copy_scenario is None:
            return {}
        return dict(scenario_id=self.copy_scenario.getId())


def ensureScenarioInTarget(scenario, target_docpool):
    """Prepare target scenario on document transfer.

    For each scenario assigned to the original, try to identify a scenario at the target
    ESD, matching by object id. Copy unmatched scenario to target ESD.

    According to #5872, make sure copied scenario is in published state.
    """
    scen = target_docpool.contentconfig.scen

    if orig_event := api.content.get(UID=scenario):
        copy_id = orig_event.id
        if scen.hasObject(copy_id):
            copy_event = scen[copy_id]
        else:
            copy_id = _copyPaste(orig_event, scen)
            copy_event = scen[copy_id]
            if api.content.get_state(copy_event) == "private":
                api.content.transition(copy_event, "publish")

        return copy_event
