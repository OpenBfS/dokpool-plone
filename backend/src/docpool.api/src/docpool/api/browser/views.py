from Acquisition import aq_base
from plone.restapi.interfaces import ISerializeToJson
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter

import json


class JSONView(BrowserView):
    def __call__(self):
        self.request.response.setHeader("Content-Type", "application/json")
        serializer = getMultiAdapter((self.context, self.request), ISerializeToJson)
        if IPloneSiteRoot.providedBy(self.context):
            item = serializer()
        elif getattr(aq_base(self.context), "isPrincipiaFolderish", False):
            item = serializer(include_items=False)
        return json.dumps(item, indent=4, sort_keys=True)
