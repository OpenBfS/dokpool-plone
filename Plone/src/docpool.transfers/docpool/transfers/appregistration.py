# -*- coding: utf-8 -*-
from Products.Archetypes.utils import shasattr

from docpool.base.appregistry import registerApp
from docpool.transfers.config import TRANSFERS_APP
from docpool.config.local.transfers import dpAdded, dpRemoved
from docpool.transfers.behaviors.transferstype import ITransfersType
from docpool.transfers.behaviors.transferable import ITransferable

registerApp(TRANSFERS_APP, u"Transfer Support", ITransfersType, ITransferable, dpAdded, dpRemoved)