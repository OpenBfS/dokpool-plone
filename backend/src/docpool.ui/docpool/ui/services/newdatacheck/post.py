from plone import api
from plone.restapi.deserializer import json_body
from plone.restapi.services import Service

import json


class Listing:
    def find(self, limit=0):
        form = self.request.form
        self.limit = int(form.get("limit", limit))

        self.dokType = form.get("dokType")
        self.documenttypes_vocabulary = api.portal.get_vocabulary(
            "docpool.base.vocabularies.DocumentTypes", self.context
        )

        query = {
            "context": self.context,
            "portal_type": "DPDocument",
            "sort_on": "modified",
            "sort_order": "reverse",
        }
        if self.limit:
            query["sort_limit"] = self.limit
        if self.dokType:
            query["dp_type"] = self.dokType

        brains = api.content.find(**query)
        uids = [brain.UID for brain in brains]
        modified = max(brain.modified for brain in brains) if brains else None

        if self.limit > 0:
            uids = uids[: self.limit]

        return uids, modified


class NewDataCheck(Listing, Service):
    def reply(self):
        _, modified = self.find()
        data = json_body(self.request)
        modified_since = json.loads(data.get("modified_since", ""))
        return {"hasNewData": (modified.timeTime() if modified else None) != modified_since}
