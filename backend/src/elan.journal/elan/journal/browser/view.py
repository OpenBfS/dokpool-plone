from DateTime import DateTime
from elan.journal.browser.base import BaseView
from plone.memoize import ram
from time import time
from zope.publisher.browser import BrowserView


def _updates_cachekey(method, self):
    return (self.context.absolute_url_path(), int(self.context.modified()))


class View(BrowserView, BaseView):

    """Default view for Journal."""

    @ram.cache(_updates_cachekey)
    def updates(self):
        """Return the list of entries in the Journal in reverse order;
        the list is cached until a new update is published.
        """
        return self.context.get_journalentries()

    @property
    def has_updates(self):
        """Return True if Journal has updates."""
        return len(self.updates()) > 0

    @property
    def automatic_updates_enabled(self):
        """Check if the Livelog must be updated automatically.
        Automatic updates are turned off if there have been no new
        journal-entries in the last 24 hours.
        """
        return (DateTime() - self.context.modified()) < 1

    @property
    def now(self):
        """Return a timestamp for the current date and time."""
        return str(time())
