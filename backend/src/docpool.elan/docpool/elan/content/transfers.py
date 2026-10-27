from docpool.base.behaviors.transferable import IAppSpecificTransfer
from docpool.base.behaviors.transferable import IAppSpecificTransferable
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


class ELANSpecificTransferRelated:
    def __init__(self, original):
        self.original = original
        self.elanobj = IELANDocument(self.original)
        self.scenario = (
            scen if (uid := self.elanobj.scenario) and (scen := api.content.get(UID=uid)) else None
        )


@adapter(IDPDocument)
@implementer(IAppSpecificTransferable)
@named(ELAN_APP)
class ELANSpecificTransferable(ELANSpecificTransferRelated):
    def assert_transferable(self):
        if self.scenario.EventType == "Minor Situation":
            raise ValueError(_("Cannot transfer entry with an event of type Minor Situation."))


@adapter(IDPDocument, IDPTransferFolder)
@implementer(IAppSpecificTransfer)
@named(ELAN_APP)
class ELANSpecificTransfer(ELANSpecificTransferRelated):
    def __init__(self, original, transfer_folder):
        super().__init__(original)
        self.transfer_folder = transfer_folder

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
