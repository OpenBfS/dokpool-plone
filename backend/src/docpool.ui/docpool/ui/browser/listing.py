from docpool.base.utils import is_rei_workflow
from docpool.ui.services.newdatacheck.post import Listing as ListingBase
from plone import api
from Products.Five.browser import BrowserView
from zope.i18n import translate

import json


class Listing(ListingBase, BrowserView):
    """Example view called from template"""

    def __call__(self, limit=0):
        uids, modified = self.find(limit)

        # Mod-Date dazu und hash über udis & mod-date
        self.items = json.dumps(uids)
        self.modified = json.dumps(modified.timeTime()) if modified else None
        return self.index()


class Item(BrowserView):
    """Example view called from template"""

    def __call__(self, uid=None):
        request = self.request
        self.uid = uid
        obj = api.content.get(UID=uid)

        portal_workflow = api.portal.get_tool("portal_workflow")
        review_state = api.content.get_state(obj)
        state_title = portal_workflow.getTitleForStateOnType(review_state, obj.portal_type)
        domain = "docpool.base"
        if is_rei_workflow(obj):
            domain = "docpool.rei"
        state_title = translate(state_title, domain=domain, context=request)

        if userinfo := obj.modified_by or obj.created_by:
            userinfo = userinfo.replace("<i>", "--separator--<i>", 1)
            user = userinfo.split("--separator--")[0]
            group = userinfo.split("--separator--")[1] if "--separator--" in userinfo else ""

        self.dpdocument = {
            "date": obj.mdate,
            "title": obj.title,
            "id": obj.id,
            "description": obj.description,
            "review_state": review_state,
            "state_title": state_title,
            "uid": uid,
            "docType": obj.docType,
            "url": obj.absolute_url(),
            "modified_by_user": user,
            "modified_by_group": group,
        }
        return self.index()
