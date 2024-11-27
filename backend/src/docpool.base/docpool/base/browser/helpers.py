from docpool.base import DocpoolMessageFactory as _
from docpool.base.utils import activateAppFilter
from docpool.base.utils import get_docpool_for_user
from docpool.base.utils import is_admin
from docpool.base.utils import is_contentadmin
from docpool.base.utils import is_individual
from docpool.base.utils import is_personal
from docpool.base.utils import setApplicationsForCurrentUser
from pkg_resources import get_distribution
from plone import api
from plone.api.exc import InvalidParameterError
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

        # 3. Redirect to users dokpool
        if obj := get_docpool_for_user(api.user.get_current()):
            return response.redirect(obj.absolute_url())

        return "No dokpool found."


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
                "rodos": "/potentially-affected-areas",
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


class ChangeState(BrowserView):
    """Change the workflow-state of any document.
    Replaces published instance-methods (#5831).
    """

    def __call__(self, uid=None, action=None, back_to_referer=False):
        alsoProvides(self.request, IDisableCSRFProtection)
        self.back_to_referer = back_to_referer
        if not action:
            return self.redirect()

        if not uid:
            obj = self.context
        else:
            obj = api.content.get(UID=uid)
            if not obj:
                return self.redirect()
        try:
            api.content.transition(obj, transition=action)
            if action == "publish":
                for subobj in obj.getDPDocuments():
                    try:
                        api.content.transition(subobj, transition=action)
                    except InvalidParameterError:
                        pass
        except InvalidParameterError:
            return self.redirect()
        api.portal.show_message(_("The document state has been changed."), self.request)
        return self.redirect()

    def redirect(self):
        if self.back_to_referer and (last_referer := self.request.get("HTTP_REFERER")):
            return self.request.response.redirect(last_referer)
        return self.context.restrictedTraverse("@@view")()
