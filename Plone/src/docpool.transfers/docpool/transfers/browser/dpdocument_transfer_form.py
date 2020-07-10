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
        self.dpdocids = dpdocids
        self.targets = targets
        if not request.form.get('form.button.submit', None):
            return self.index()

        if not dpdocids or not targets:
            api.portal.show_message('Not items or targets selected!', request)
            return self.index()

        if dpdocids and targets:
            message = self.transfer_documents()
            if message:
                api.portal.show_message(message, request)
                return self.index()
            else:
                api.portal.show_message('{} Items transfered!'.format(len(dpdocids)), request)
                request.response.redirect(self.context.absolute_url())
        return self.index()

    def transfer_infos(self):
        targets = []
        items = []
        # the folder_listing passes paths
        paths = self.request.get('paths', [])
        if not paths and self.dpdocids:
            # handle individual transfer
            paths = self.dpdocids
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

    def transfer_documents(self):
        for dpdocid in self.dpdocids:
            doc = self.context._getOb(dpdocid)
            dpdoc = doc.doc_extension(TRANSFERS_APP)
            dpdoc.manage_transfer(self.targets)
            log("Transfer %s to ChannelIDs: %s" % (doc.title, self.targets))
        return
