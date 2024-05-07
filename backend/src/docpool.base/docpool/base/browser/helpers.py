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

        # 1. Anonymous users must login
        if api.user.is_anonymous():
            return response.redirect(self.context.absolute_url() + "/login")

        # 2. Admins get folder_contents
        is_admin = {"Manager", "Site Administrator"} & set(api.user.get_roles())
        if is_admin:
            return response.redirect(self.context.absolute_url() + "/folder_contents")

        # 3. Normal users have a dp assigned to them. Redirect to it.
        current_user = api.user.get_current()
        if dp_uid := current_user.getProperty("dp"):
            if obj := api.content.get(UID=dp_uid):
                return response.redirect(obj.absolute_url())

        # 4. No dp's or user without access to any dp.
        brains = api.content.find(portal_type="DocumentPool", sort_on="sortable_title")
        if not brains:
            return "No dokpool found."

        # 5. Some users have the id of a dp as prefix. Redirect to that.
        username = current_user.getUserName()
        user_prefix = username.split("_")[0]
        dokpool_prefix = user_prefix if username != user_prefix else None
        if dokpool_prefix:
            for brain in brains:
                obj = brain.getObject()
                if obj.myPrefix() == dokpool_prefix:
                    return response.redirect(obj.absolute_url())

        # 6. Fallback to first available dp
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
    @property
    def admin(self):
        return is_admin(self.context)

    @property
    def contentadmin(self):
        return is_contentadmin(self.context)

    @property
    def admin_or_contentadmin(self):
        # TODO re #5547: check whether this is still useful after cleaning up conditions
        return is_admin(self.context) or is_contentadmin(self.context)

    @property
    def archive(self):
        return "archive" in self.context.getPhysicalPath()

    @property
    def individual(self):
        return is_individual(self.context)

    @property
    def personal(self):
        return is_personal(self.context)
