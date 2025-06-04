from Products.Five.browser import BrowserView
from plone import api
import json


class Listing(BrowserView):
    """Example view called from template"""

    def __call__(self, limit=0):
        form = self.request.form
        self.limit = int(form.get('limit', limit))

        # Do we fetch form catalog? UUIDs?
        dp_documents = api.content.find(context=self.context, portal_type="DPDocument")
        uids = [brain.UID for brain in dp_documents]

        if self.limit > 0:
            uids = uids[:self.limit]

        self.items = json.dumps(uids)
        return self.index()


class Item(BrowserView):
    """Example view called from template"""

    def __call__(self, uid=None):
        self.uid = uid
        dpdocument_obj = api.content.get(UID=uid)
        self.dpdocument = {"title": dpdocument_obj.title, "id": uid, "docType": dpdocument_obj.docType,
                           "url": dpdocument_obj.absolute_url()}
        return self.index()
