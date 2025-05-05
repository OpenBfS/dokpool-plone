from docpool.base import DocpoolMessageFactory as _
from docpool.base.behaviors.transferable import ITransferable
from docpool.base.config import TRANSFERS_APP
from plone import api
from Products.CMFPlone.utils import log
from Products.Five.browser import BrowserView
from zope.i18nmessageid import MessageFactory


PMF = MessageFactory("plone")


class TransferForm(BrowserView):
    def __call__(self, dpdocids=None, targets=None):
        request = self.request
        self.dpdocids = dpdocids

        if request.form.get("form.button.cancel"):
            msg = PMF("Changes canceled.")
            api.portal.show_message(msg, self.request)
            return request.response.redirect(self.context.absolute_url())

        if not request.form.get("form.button.submit", None):
            return self.index()

        if not dpdocids or not targets:
            api.portal.show_message(_("No items or targets selected!"), request)
            return self.index()

        for dpdocid in dpdocids:
            doc = api.content.get(path=dpdocid)
            dpdoc = doc.doc_extension(TRANSFERS_APP)
            dpdoc.transferToTargets(targets)
            log(f'Transfer "{doc.title}" to transfer folders {targets}')

        msg = _("${transferred} Items transferred!", mapping={"transferred": len(dpdocids)})
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

        target_infos = []
        portal_catalog = api.portal.get_tool("portal_catalog")
        for target in set(targets):
            # ContentSenders do not need access to the target folders!
            brains = portal_catalog.unrestrictedSearchResults(UID=target)
            obj = brains[0]._unrestrictedGetObject()
            to_title = obj.myDocumentPool().title
            target_infos.append({"id": target, "esd_to_title": to_title})
        return {
            "items": items,
            "targets": sorted(target_infos, key=lambda x: x["esd_to_title"]),
        }
