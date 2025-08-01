from plone import api
from plone.memoize import view


class BaseView:
    """Base view with helper methods for Journal."""

    @property
    @view.memoize
    def is_anonymous(self):
        return api.user.is_anonymous()

    @property
    @view.memoize
    def show_byline(self):
        """Return True if user is allowed to view 'about' information."""
        allow_view = api.portal.get_registry_record("plone.allow_anon_views_about")
        return not self.is_anonymous or allow_view
