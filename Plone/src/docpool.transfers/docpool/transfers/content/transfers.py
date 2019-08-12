# -*- coding: utf-8 -*-
from docpool.base.utils import _copyPaste
from docpool.base.utils import queryForObject
from docpool.dbaccess.dbinit import __session__
from docpool.transfers.db.model import Channel
from Products.CMFCore.utils import getToolByName


HAS_ELAN = True
try:
    from docpool.elan.config import ELAN_APP
except:
    HAS_ELAN = False


def determineChannels(transfer_ids):
    channels = __session__.query(Channel).filter(Channel.id.in_(transfer_ids)).all()
    return channels


def determineTransferFolderObject(self, channel):
    uid = channel.tf_uid
    return queryForObject(self, UID=uid)


def ensureDocTypeInTarget(original, copy):
    my_dt = original.docType
    config = copy.myDocumentPool().config.dtypes
    if config.hasObject(my_dt):
        return
    dtObj = original.docTypeObj()
    id = _copyPaste(dtObj, config)
    new_dt = config._getOb(id)
    if HAS_ELAN:
        new_dt.doc_extension(ELAN_APP).setCCategory(
            'recent'
        )  # Set intermediate category
    wftool = getToolByName(original, 'portal_workflow')
    wftool.doActionFor(new_dt, 'retract')
    new_dt.reindexObject()
    new_dt.reindexObjectSecurity()
    config.reindexObject()
