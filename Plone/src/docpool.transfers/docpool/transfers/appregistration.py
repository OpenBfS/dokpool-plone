# -*- coding: utf-8 -*-
from Products.Archetypes.utils import shasattr

from docpool.base.appregistry import registerApp
from docpool.transfers.config import TRANSFERS_APP

def createTransfersType(self):
    if not shasattr(self, TRANSFERS_APP, acquire=False):
        self.invokeFactory(id=TRANSFERS_APP, type_name="TransfersType", title="TransfersType")

def createTransferable(self):
    if not shasattr(self, TRANSFERS_APP, acquire=False):
        self.invokeFactory(id=TRANSFERS_APP, type_name="Transferable", title="Transferable")

registerApp(TRANSFERS_APP, createTransfersType, createTransferable)