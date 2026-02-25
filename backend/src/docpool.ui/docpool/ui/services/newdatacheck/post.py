from plone import api
from plone.restapi.services import Service


class NewDataCheck(Service):
    def reply(self):
        listing = api.content.get_view("listing", self.context, self.request)
        _, modified, _ = listing.find(limit=0)
        return {"modified_last": (modified.timeTime() if modified else None)}
