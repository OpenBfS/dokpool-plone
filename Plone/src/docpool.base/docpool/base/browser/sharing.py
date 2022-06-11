from Acquisition import aq_parent
from plone.app.workflow import PloneMessageFactory as _
from plone.app.workflow.browser.sharing import SharingView as OSV
from plone.base.utils import safe_text
from plone.memoize.instance import memoize
from zope.component import getMultiAdapter
from zope.i18n import translate


class SharingView(OSV):
    @memoize
    def roles(self):
        """
        Reduce the available roles for sharing
        """
        pairs = OSV.roles(self)
        return [p for p in pairs if p["id"] == "Reader"]

    def _principal_search_results(
        self,
        search_for_principal,
        get_principal_by_id,
        get_principal_title,
        principal_type,
        id_key,
    ):
        """Return search results for a query to add new users or groups.

        Returns a list of dicts, as per role_settings().

        Arguments:
            search_for_principal -- a function that takes an IPASSearchView and
                a search string. Uses the former to search for the latter and
                returns the results.
            get_principal_by_id -- a function that takes a user id and returns
                the user of that id
            get_principal_title -- a function that takes a user and a default
                title and returns a human-readable title for the user. If it
                can't think of anything good, returns the default title.
            principal_type -- either 'user' or 'group', depending on what kind
                of principals you want
            id_key -- the key under which the principal id is stored in the
                dicts returned from search_for_principal
        """
        context = self.context

        translated_message = translate(
            _("Search for user or group"), context=self.request
        )
        search_term = safe_text(self.request.form.get("search_term", None))
        if not search_term or search_term == translated_message:
            return []

        existing_principals = {
            p["id"]
            for p in self.existing_role_settings()
            if p["type"] == principal_type
        }
        empty_roles = {r["id"]: False for r in self.roles()}
        info = []

        # BfS: we need the Plone Site here, because we want to see ALL groups
        hunter = getMultiAdapter((aq_parent(context), self.request), name="pas_search")

        for principal_info in search_for_principal(hunter, search_term):
            principal_id = principal_info[id_key]
            if principal_id not in existing_principals:
                principal = get_principal_by_id(principal_id)
                roles = empty_roles.copy()
                if principal is None:
                    continue

                for r in principal.getRoles():
                    if r in roles:
                        roles[r] = "global"
                login = principal.getUserName()
                if principal_type == "group":
                    login = None
                info.append(
                    dict(
                        id=principal_id,
                        title=get_principal_title(principal, principal_id),
                        login=login,
                        type=principal_type,
                        roles=roles,
                    )
                )
        return info
