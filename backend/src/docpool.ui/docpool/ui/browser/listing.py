import json

from docpool.ui.services.newdatacheck.post import Listing as ListingBase
from plone import api
from Products.Five.browser import BrowserView


class Listing(ListingBase, BrowserView):
    """Example view called from template"""

    def __call__(self, limit=0):
        uids, modified = self.find(limit)

        # Mod-Date dazu und hash über udis & mod-date
        self.items = json.dumps(uids)
        self.modified = json.dumps(modified.timeTime())
        return self.index()


class Item(BrowserView):
    """Example view called from template"""

    def __call__(self, uid=None):
        self.uid = uid
        dpdocument_obj = api.content.get(UID=uid)
        self.dpdocument = {
            "title": dpdocument_obj.title,
            "wf_status": api.content.get_state(dpdocument_obj),
            "id": uid,
            "docType": dpdocument_obj.docType,
            "url": dpdocument_obj.absolute_url(),
        }
        return self.index()
