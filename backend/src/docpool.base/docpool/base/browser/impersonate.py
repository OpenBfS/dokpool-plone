from collective.impersonate.browser.impersonate import Impersonate
from plone import api


class Impersonate(Impersonate):
    """Override @@impersonate view to redirect to portal and show users."""

    def actions(self):
        """Login the user"""
        if "username" in list(self.request.keys()):
            self.errors = {}
            username = self.request["username"].strip()
            if not api.user.get(username=username):
                self.errors["username"] = username
                return

            self.context.acl_users.session._setupSession(username, self.context.REQUEST.RESPONSE)

            # Patch: redirect to portal
            self.request.RESPONSE.redirect(api.portal.get().absolute_url())

    @property
    def many_users(self):
        # Patch: list all users
        return False
