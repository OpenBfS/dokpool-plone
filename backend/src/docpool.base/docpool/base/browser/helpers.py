from docpool.base.utils import activateAppFilter
from docpool.base.utils import is_admin
from docpool.base.utils import is_contentadmin
from docpool.base.utils import is_individual
from docpool.base.utils import is_personal
from docpool.base.utils import setApplicationsForCurrentUser
from pkg_resources import get_distribution
from plone import api
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five import BrowserView
from zope.interface import alsoProvides


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


class DocPoolURL(BrowserView):
    def __call__(self):
        if (dp := getattr(self.context, "myDocumentPool", None)) is not None:
            return dp().absolute_url()
        else:
            return self.context.portal_url()


class ActivateAppFilter(BrowserView):
    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        activate = self.request.get("activateFilter", False)
        activateAppFilter(self.context, activate)
        return self.request.response.redirect(self.context.absolute_url())


class SetActiveApp(BrowserView):
    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        context = self.context
        app = self.request.get("app")
        setApplicationsForCurrentUser(context, [app])
        activateAppFilter(context, True)
        absurl = context.absolute_url()
        if "content" not in absurl:
            suffixes = {
                "base": "",
                "elan": "/esd",
                "doksys": "/searches",
                "rei": "/berichte",
                "rodos": "/rodos",
            }
            if (suffix := suffixes.get(app)) is not None:
                absurl = context.myDocumentPool().absolute_url() + suffix
        return self.request.response.redirect(absurl)


class Is(BrowserView):
    def admin(self):
        return is_admin(self.context)

    def contentadmin(self):
        return is_contentadmin(self.context)

    def admin_or_contentadmin(self):
        # TODO re #5547: check whether this is still useful after cleaning up conditions
        return is_admin(self.context) or is_contentadmin(self.context)

    def archive(self):
        return "archive" in self.context.getPhysicalPath()

    def individual(self):
        return is_individual(self.context)

    def personal(self):
        return is_personal(self.context)
