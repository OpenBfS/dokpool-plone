from docpool.base.appregistry import registerApp
from docpool.base.behaviors.transferable import ITransferable
from docpool.base.behaviors.transferstype import ITransfersType
from docpool.base.config import BASE_APP
from docpool.base.config import TRANSFERS_APP
from docpool.config.local.base import dpAdded
from docpool.config.local.base import dpRemoved
from docpool.config.local.transfers import dpAdded as transfers_added
from docpool.config.local.transfers import dpRemoved as transfers_removed


registerApp(BASE_APP, "Docpool Base", None, None, dpAdded, dpRemoved)
# "None" means: no extension support

# Transfers are always available
registerApp(
    TRANSFERS_APP,
    "Transfer Support",
    ITransfersType,
    ITransferable,
    transfers_added,
    transfers_removed,
    implicit=True,
)
