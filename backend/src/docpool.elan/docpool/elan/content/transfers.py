from docpool.base.behaviors.transferable import IAppSpecificTransfer
from docpool.base.content.dpdocument import IDPDocument
from docpool.base.content.dptransferfolder import IDPTransferFolder
from docpool.base.utils import _copyPaste
from docpool.elan.behaviors.elandocument import IELANDocument
from docpool.elan.config import ELAN_APP
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
        self.have_elan = ELAN_APP in self.transfer_folder.myDocumentPool().supportedApps

    def assert_allowed(self):
        return

    def sender_log_entry(self):
        scenario_ids = ", ".join(b.getId for b in api.content.find(UID=self.elanobj.scenarios))
        return dict(scenario_ids=scenario_ids)

    def __call__(self, copy):
        if not self.have_elan:
            try:
                del copy.aq_base.scenarios
            except AttributeError:
                pass
            return

        self.copy_scenarios = list(ensureScenariosInTarget(self.elanobj.scenarios, copy.myDocumentPool()))
        try:
            IELANDocument(copy).scenarios = [s.UID() for s in self.copy_scenarios]
        except Exception as e:
            log_exc(e)

    def receiver_log_entry(self):
        if not self.have_elan:
            return {}
        return dict(scenario_ids=", ".join(s.getId() for s in self.copy_scenarios))


def ensureScenariosInTarget(scenarios, target_docpool):
    """Prepare target scenarios on document transfer.

    For each scenario assigned to the original, try to identify a scenario at the target
    ESD, matching by object id. Copy unmatched scenarios to target ESD.

    According to #5872, make sure copied scenarios are in published state.
    """
    scen = target_docpool.contentconfig.scen

    for orig_brain in api.content.find(UID=scenarios):
        copy_id = orig_brain.getId
        if scen.hasObject(copy_id):
            copy_event = scen[copy_id]
        else:
            orig_event = orig_brain.getObject()
            copy_id = _copyPaste(orig_event, scen)
            copy_event = scen[copy_id]
            if api.content.get_state(copy_event) == "private":
                api.content.transition(copy_event, "publish")

        yield copy_event
