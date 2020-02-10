# -*- coding: UTF-8 -*-
from Products.CMFPlone import MessageFactory
from Products.CMFPlone.utils import log, log_exc
from docpool.transfers.config import TRANSFERS_APP
from Products.Five.browser import BrowserView
from docpool.transfers import DocpoolMessageFactory as _


class TransferForm(BrowserView):


    def __call__(self, dpdocid=None, targets=None):
        request = self.request
        if not request.get('sumbit'):
            return self.index()

        if not dpdocid or not targets:
            api.portal.show_message('Not items or targets selected!', request)
            return self.index()

        message = self.transfer_documents(dpdocid, targetIds)
        if message:
            api.portal.show_message(message, request)
            return self.index()

        api.portal.show_message('{} Items transfered!'.format(len(dpdocid)), request)
        request.response.redirect(self.context.absolute_url())


    def getTransferInfos(self):
        dpdocid = self.request.get('id')
        doc = self.context._getOb(dpdocid)
        return dpdocid, doc, doc.doc_extension(TRANSFERS_APP)


    def transfer_documents(self, dpdocid, targetIds):

        doc = self._getOb(dpdocid)
        dpdoc = doc.doc_extension(TRANSFERS_APP)
        dpdoc.manage_transfer(targetIds)
        log("Transfer %s to ChannelIDs: %s" % (doc.Title(), targetIds))
        return
