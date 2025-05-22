from Acquisition import aq_get
from docpool.base.utils import getUserInfo
from plone import api
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ELANArchivesView(BrowserView):
    """Default view"""

    __call__ = ViewPageTemplateFile("elanarchives.pt")

    def get_archives(self):
        """ """
        query = {
            "portal_type": "ELANArchive",
            "sort_on": "modified",
            "sort_order": "reverse",
        }
        return [obj.getObject() for obj in api.content.find(context=self.context, **query)]

    def number_of_entries(self, archive):
        contentarea = aq_get(archive, "content")
        args = {
            "portal_type": "DPDocument",
        }
        return len(api.content.find(context=contentarea, **args))

    def get_user_info_string(self, username):
        userid, fullname, primary_group = getUserInfo(self.context, username)
        if primary_group:
            return fullname + f" <i>{primary_group}</i>"
        return fullname
