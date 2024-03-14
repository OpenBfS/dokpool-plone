from pkg_resources import get_distribution
from plone import api
from Products.Five import BrowserView


class DokpoolVersion(BrowserView):
    def __call__(self):
        dist = get_distribution("docpool.base")
        return dist.version


class RootRedirectView(BrowserView):
    """Redirect to the users dokpool."""

    def __call__(self):
        response = self.request.response
        if api.user.is_anonymous():
            return response.redirect(self.context.absolute_url() + "/login")

        is_admin = {"Manager", "Site Administrator"} & set(api.user.get_roles())
        if is_admin:
            return response.redirect(self.context.absolute_url() + "/folder_contents")

        brains = api.content.find(portal_type="DocumentPool", sort_on="sortable_title")
        if not brains:
            return "No dokpool found."

        username = api.user.get_current().getUserName()
        user_prefix = username.split("_")[0]
        dokpool_prefix = user_prefix if username != user_prefix else None
        if dokpool_prefix:
            for brain in brains:
                obj = brain.getObject()
                if obj.myPrefix() == dokpool_prefix:
                    return response.redirect(obj.absolute_url())
        return response.redirect(brains[0].getPath())