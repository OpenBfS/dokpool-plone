from docpool.base import DocpoolMessageFactory as _
from docpool.base.behaviors.transferable import ITransferable
from docpool.transfers.config import TRANSFERS_APP
from plone import api
from Products.CMFPlone.utils import log
from Products.Five.browser import BrowserView


class TransferForm(BrowserView):
    def __call__(self, dpdocids=None, targets=None):
        request = self.request
        self.dpdocids = dpdocids
        if not request.form.get("form.button.submit", None):
            return self.index()

        if not dpdocids or not targets:
            api.portal.show_message(_("No items or targets selected!"), request)
            return self.index()

        for dpdocid in dpdocids:
            doc = self.context._getOb(dpdocid)
            dpdoc = doc.doc_extension(TRANSFERS_APP)
            dpdoc.transferToTargets(targets)
            log(f'Transfer "{doc.title}" to transfer folders {targets}')

        msg = _(
            "${transferred} Items transferred!", mapping={"transferred": len(dpdocids)}
        )
        api.portal.show_message(msg, request)
        request.response.redirect(self.context.absolute_url())
        return self.index()

    def transfer_infos(self):
        targets = []
        items = []
        # the folder_listing passes paths
        paths = self.request.get("paths", [])
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
            if adapted.transferable() and (allowed := adapted.allowedTargets()):
                targets.extend(allowed)
                items.append(obj)

        to_title = lambda target: api.content.get(UID=target).myDocumentPool().Title()
        return dict(
            items=items,
            targets=[
                dict(id=target, esd_to_title=to_title(target))
                for target in set(targets)
            ],
        )
