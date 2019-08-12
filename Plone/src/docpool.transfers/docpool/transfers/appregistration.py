# -*- coding: utf-8 -*-

from docpool.base.appregistry import registerApp
from docpool.config.local.transfers import dpAdded
from docpool.config.local.transfers import dpRemoved
from docpool.transfers.behaviors.transferable import ITransferable
from docpool.transfers.behaviors.transferstype import ITransfersType
from docpool.transfers.config import TRANSFERS_APP


# Transfers are always available
registerApp(
    TRANSFERS_APP,
    u"Transfer Support",
    ITransfersType,
    ITransferable,
    dpAdded,
    dpRemoved,
    implicit=True,
)
