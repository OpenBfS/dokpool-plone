from docpool.base import DocpoolMessageFactory as _
from docpool.base.content.dpdocument import IDPDocument
from docpool.base.utils import activateAppFilter
from docpool.base.utils import get_docpool_for_user
from docpool.base.utils import is_admin
from docpool.base.utils import is_contentadmin
from docpool.base.utils import is_individual
from docpool.base.utils import is_personal
from docpool.base.utils import is_rei_workflow
from docpool.base.utils import setApplicationsForCurrentUser
from importlib.metadata import distribution
from plone import api
from plone.api.exc import InvalidParameterError
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Five import BrowserView
from zope.component import getMultiAdapter
from zope.interface import alsoProvides

import logging


log = logging.getLogger(__name__)


class DokpoolVersion(BrowserView):
    def __call__(self):
        dist = distribution("docpool.base")
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
        if app not in ["base", "doksys", "elan", "rei", "rodos"]:
            # prevent invalid apps (#5996)
            return self.request.response.redirect(context.absolute_url())
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

    def rei_workflow(self):
        # rei workflow is only possible on dpdocument
        if IDPDocument.providedBy(self.context):
            return is_rei_workflow(self.context)
        else:
            log.info("Rei WF only possible on dpdocument")


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
        return self.request.response.redirect(self.context.absolute_url())


class CanChangePassword(BrowserView):
    def __call__(self):
        portal_state = getMultiAdapter(
            (self.context, self.request), name="plone_portal_state"
        )

        member = portal_state.member()
        # IMIS-Users uses SSO and cannot change their password
        if member.getId()[:2] == "i-":
            return False

        # User with only these roles should not change their password.
        # They are usually shared by multiple people.
        # FIXME: THIS DOES NOT WORK ! - also users which can add portal content in their group do only have these groups
        # roles = member.getRolesInContext(self.context)
        # read_only = ['Member', 'Authenticated', 'ELANUser', 'Reader']
        # can_change_pwd_roles = [r for r in roles if r not in read_only]
        # return bool(can_change_pwd_roles)

        # read only ELAN-Users
        # usually shared by multiple people
        if (member.getId()[-2:] == "-u") or (member.getId()[-5:] == "-info"):
            return False

        return True
