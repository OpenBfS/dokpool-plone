# -*- coding: utf-8 -*-
from docpool.base.content.dpdocument import IDPDocument
from docpool.rei.behaviors.reidoc import IREIDoc
from plone.base.utils import safe_bytes
from plone.indexer import indexer

import six


# TODO: Remove after upgrade to Python 3
@indexer(IDPDocument)
def Origins(obj):
    reidoc = IREIDoc(obj, None)
    if not reidoc:
        return
    if not reidoc.Origins:
        return []
    if six.PY2:
        return [safe_bytes(s) for s in reidoc.Origins]
    return reidoc.Origins
