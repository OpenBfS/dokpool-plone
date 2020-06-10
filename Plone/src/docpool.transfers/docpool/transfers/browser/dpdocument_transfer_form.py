# -*- coding: UTF-8 -*-
from plone import api
from Products.CMFPlone import MessageFactory
from Products.CMFPlone.utils import log, log_exc
from docpool.transfers.config import TRANSFERS_APP
from Products.Five.browser import BrowserView
from docpool.transfers import DocpoolMessageFactory as _
from docpool.transfers.behaviors.transferable import ITransferable


class TransferForm(BrowserView):


    def __call__(self, dpdocids=None, targets=None):
        request = self.request
        if not request.get('form.button.submit'):
            return self.index()

        if not dpdocids or not targets:
            api.portal.show_message('Not items or targets selected!', request)
            return self.index()

        message = self.transfer_documents(dpdocids, targets)
        if message:
            api.portal.show_message(message, request)
            return self.index()

        api.portal.show_message('{} Items transfered!'.format(len(dpdocids)), request)
        request.response.redirect(self.context.absolute_url())

    def getTransferInfos(self):
        infos = []
        paths = self.request.get('paths', [])
        for path in paths:
            obj = api.content.get(path=path)
            if not obj:
                continue
            try:
                adapted = ITransferable(obj)
            except TypeError:
                continue
            if adapted.transferable() and adapted.allowedTargets():
                infos.append((obj.id, obj, adapted))
        return infos

    def transfer_infos(self):
        targets = []
        items = []
        paths = self.request.get('paths', [])
        for path in paths:
            obj = api.content.get(path=path)
            if not obj:
                continue
            try:
                adapted = ITransferable(obj)
            except TypeError:
                continue
            if adapted.transferable() and adapted.allowedTargets():
                targets.extend(adapted.allowedTargets())
                items.append(obj)
        return {'items': items, 'targets': set(targets)}

    def transfer_documents(self, dpdocids, targetIds):
        for dpdocid in dpdocids:
            doc = self.context._getOb(dpdocid)
            dpdoc = doc.doc_extension(TRANSFERS_APP)
            dpdoc.manage_transfer(targetIds)
            log("Transfer %s to ChannelIDs: %s" % (doc.title, targetIds))
        return
