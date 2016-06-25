# -*- coding: utf-8 -*-
from Products.Archetypes.utils import shasattr

from docpool.base.appregistry import registerApp, createTypeObject, createDocumentObject
from docpool.elan.config import ELAN_APP
from docpool.transfers.config import TRANSFERS_APP


def createELANType(self):
    if not shasattr(self, ELAN_APP, acquire=False):
        self.invokeFactory(id=ELAN_APP, type_name="ELANType", title="ELANType")
    createTypeObject(TRANSFERS_APP, self)

def createELANDocument(self):
    if not shasattr(self, ELAN_APP, acquire=False):
        self.invokeFactory(id=ELAN_APP, type_name="ELANDocument", title="ELANDocument")
    createDocumentObject(TRANSFERS_APP, self)

registerApp(ELAN_APP, createELANType, createELANDocument)