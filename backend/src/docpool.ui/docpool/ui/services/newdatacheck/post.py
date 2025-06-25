import json

from plone import api
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service


class Listing:
    def find(self, limit=0):
        form = self.request.form
        self.limit = int(form.get("limit", limit))

        # Do we fetch form catalog? UUIDs?
        dp_documents = api.content.find(
            context=self.context,
            portal_type="DPDocument",
            sort_on="modified",
            sort_order="reverse",
        )
        uids = [brain.UID for brain in dp_documents]
        modified = max(brain.modified for brain in dp_documents)

        if self.limit > 0:
            uids = uids[: self.limit]

        return uids, modified


class NewDataCheck(Listing, Service):
    def reply(self):
        _, modified = self.find()
        data = json_body(self.request)
        modified_since = json.loads(data.get("modified_since", ""))
        return {"hasNewData": modified.timeTime() != modified_since}
