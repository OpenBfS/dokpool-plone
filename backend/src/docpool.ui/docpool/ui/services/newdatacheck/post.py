from plone.restapi.deserializer import json_body
from plone.restapi.services import Service

import json

class NewDataCheck(Service):
    def reply(self):
        data = json_body(self.request)
        query = data.get("query", "")
        return json.dumps({"hasNewData": "true"})
