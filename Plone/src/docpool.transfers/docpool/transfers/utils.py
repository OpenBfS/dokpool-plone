# -*- coding: utf-8 -*- 
from docpool.transfers.config import TRANSFERS_APP

def getTupleForTransfer(self, id):
    """
    """
    doc = self._getOb(id)
    return doc, doc.doc_extension(TRANSFERS_APP)
