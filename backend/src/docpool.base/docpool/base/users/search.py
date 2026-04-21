from plone.protect.interfaces import IDisableCSRFProtection
from Products.CMFCore.utils import getToolByName
from Products.PlonePAS.browser.search import PASSearchView as PSV
from zope.interface import alsoProvides


class PASSearchView(PSV):
    def searchUsers(self, sort_by=None, **criteria):
        alsoProvides(self.context.REQUEST, IDisableCSRFProtection)
        self.pas = getToolByName(self.context, "acl_users")
        results = self.merge(self.pas.searchUsers(**criteria), "userid")
        if sort_by is not None:
            results = self.sort(results, sort_by)
        filtered_results = []
        if results:
            uid = self.context.UID()
            for data in results:
                # pas.getUserById is 2x faster than portal_membership.getMemberById and finds the same!
                user = self.pas.getUserById(data["id"])
                # Also ignore users without principal object!
                if user and user.getProperty("dp") == uid:
                    filtered_results.append(data)
        return filtered_results

    def searchGroups(self, sort_by=None, **criteria):
        alsoProvides(self.context.REQUEST, IDisableCSRFProtection)
        self.pas = getToolByName(self.context, "acl_users")
        gtool = getToolByName(self, "portal_groups")
        results = self.merge(self.pas.searchGroups(**criteria), "groupid")
        if sort_by is not None:
            results = self.sort(results, sort_by)
        return [r for r in results if gtool.getGroupById(r["id"]).getProperty("dp") == self.context.UID()]
