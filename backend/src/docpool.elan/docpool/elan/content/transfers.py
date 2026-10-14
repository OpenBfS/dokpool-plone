from docpool.base.behaviors.transferable import IAppSpecificTransfer
from docpool.base.content.dpdocument import IDPDocument
from docpool.base.content.dptransferfolder import IDPTransferFolder
from docpool.base.content.places import IPlaces
from docpool.elan import DocpoolMessageFactory as _
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
        self.elanobj = IELANDocument(self.original)
        self.scenario = (
            scen if (uid := self.elanobj.scenario) and (scen := api.content.get(UID=uid)) else None
        )

    def assert_allowed(self):
        if self.scenario is None:
            return

        target_docpool = IPlaces(self.transfer_folder).document_pool
        scen = target_docpool.contentconfig.scen
        if self.scenario.UID() not in scen.subscribed_events:
            raise ValueError(
                _(
                    "Cannot transfer entry to docpool without event ${event}.",
                    mapping=dict(event=self.scenario.Title()),
                )
            )

    def sender_log_entry(self):
        return dict(scenario_id=self.scenario.getId())

    def __call__(self, copy):
        IELANDocument(copy).scenario = self.scenario.UID() if self.scenario else None

    def receiver_log_entry(self):
        if self.scenario is None:
            return {}
        return dict(scenario_id=self.scenario.getId())
