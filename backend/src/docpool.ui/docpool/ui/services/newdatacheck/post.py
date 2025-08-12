from plone import api
from plone.restapi.services import Service


class Listing:
    def find(self, limit=0):
        form = self.request.form
        self.limit = int(form.get("limit", limit))

        self.selected_doktypes = form.get("selected_doktypes") or []
        self.documenttypes_vocabulary = api.portal.get_vocabulary(
            "docpool.base.vocabularies.DocumentTypes", self.context
        )

        query = {
            "context": self.context,
            "portal_type": "DPDocument",
            "sort_on": "mdate",
            "sort_order": "reverse",
        }
        if self.limit:
            query["sort_limit"] = self.limit
        if self.selected_doktypes:
            query["dp_type"] = self.selected_doktypes

        brains = api.content.find(**query)
        uids = [brain.UID for brain in brains]
        modified = max(brain.modified for brain in brains) if brains else None

        if self.limit > 0:
            uids = uids[: self.limit]

        return uids, modified


class NewDataCheck(Listing, Service):
    def reply(self):
        _, modified = self.find()
        return {"modified_last": (modified.timeTime() if modified else None)}
