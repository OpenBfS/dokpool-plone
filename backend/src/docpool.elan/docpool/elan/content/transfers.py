from docpool.base.behaviors.transferable import IAppSpecificTransfer
from docpool.base.content.dpdocument import IDPDocument
from docpool.base.content.dptransferfolder import IDPTransferFolder
from docpool.base.content.places import IPlaces
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
        self.have_elan = ELAN_APP in IPlaces(self.transfer_folder).document_pool.supportedApps
        self.scenario = (
            scen if (uid := self.elanobj.scenario) and (scen := api.content.get(UID=uid)) else None
        )

    def assert_allowed(self):
        return

    def sender_log_entry(self):
        return dict(scenario_id=self.scenario.getId())

    def __call__(self, copy):
        if not self.have_elan:
            try:
                del copy.aq_base.scenario
            except AttributeError:
                pass
            return

        (elan_copy := IELANDocument(copy)).scenario = None
        if not self.scenario:
            return

        elan_copy.scenario = self.scenario.UID()

    def receiver_log_entry(self):
        if not self.have_elan or self.scenario is None:
            return {}
        return dict(scenario_id=self.scenario.getId())
