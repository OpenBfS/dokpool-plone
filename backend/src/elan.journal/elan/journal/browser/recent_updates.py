from datetime import datetime
from elan.journal import _
from elan.journal.browser.base import BaseView
from elan.journal.logger import logger
from time import time
from zope.datetime import rfc1123_date
from zope.i18n import translate
from zope.publisher.browser import BrowserView
from zope.security import checkPermission


class RecentUpdates(BrowserView, BaseView):

    """Helper view for Journal."""

    def _needs_hard_refresh(self):
        """Return True if a hard refresh of the page is needed.

        Typically, we will request a hard refresh if a journalentry has
        been edited of deleted in the last minute.
        We set an HTTP status code 205 (Reset Content) to handle it on
        the view and update pages using JavaScript.
        """
        if self.context._last_journalentry_edition > str(time() - 60):
            logger.debug(
                "A journal entry was deleted withing the last minute. "
                "Setting status code 205."
            )
            self.request.RESPONSE.setStatus(205)
            return True

        if self.context._last_journalentry_deletion > str(time() - 60):
            logger.debug(
                "A journal entry was edited withing the last minute. "
                "Setting status code 205."
            )
            self.request.RESPONSE.setStatus(205)
            return True

    def _not_modified(self):
        """Return True and set a status code of 304 (Not Modified) if the
        requested variant has not been modified since the time specified.
        """
        header = self.request.get_header("If-Modified-Since", None)
        if header is not None:
            # do what RFC 2616 tells to do in case of invalid date
            # http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html
            header = header.split(";")[0]
            try:
                # parse RFC 1123 format and normalize for comparison
                mod_since = datetime.strptime(header, "%a, %d %b %Y %H:%M:%S %Z")
                mod_since = mod_since.strftime("%Y-%m-%d %H:%M:%S")
            except (TypeError, ValueError):
                mod_since = None
                logger.debug("If-Modified-Since header was not valid.")
            if mod_since is not None:
                logger.debug("Requesting page if modified since " + mod_since)
                # convert to UTC and normalize for comparison
                modified = self.context.modified().utcdatetime()
                modified = modified.strftime("%Y-%m-%d %H:%M:%S")
                logger.debug("Last modification occurred on " + modified)
                if modified <= mod_since:
                    logger.debug("Setting status code 304.")
                    self.request.RESPONSE.setStatus(304)  # not modified
                    return True
        logger.debug("No If-Modified-Since header on the request.")

    def __call__(self):
        logger.debug("Processing request from " + self.request.environ["REMOTE_ADDR"])

        if self._needs_hard_refresh():
            return ""

        if self._not_modified():
            return ""

        # the Expires header will help us control how often clients
        # will ask for a page; this supercedes the value defined on our
        # JavaScript code so, if we put here a value above 1 minute,
        # clients will wait that time before requesting the page again
        expires = rfc1123_date(time() + 59)  # page expires in 59 seconds
        last_modified = rfc1123_date(self.context.modified())
        self.request.RESPONSE.setHeader("Cache-Control", "public")
        self.request.RESPONSE.setHeader("Expires", expires)
        self.request.RESPONSE.setHeader("Last-Modified", last_modified)

        # https://github.com/plone/plone.protect/issues/64
        self.latest_journalentries = self.get_latest_journalentries()
        if len(self.latest_journalentries) == 0:
            return ""

        return self.index()

    # FIXME: caching this function will speed up the rendering of this
    #        view by at least an order of magnitude, but it will also
    #        create an issue: on the update view, the latest updates
    #        will lose the Delete action as a consequence of the
    #        removal of duplicated journalentries and the mixing of
    #        anonymous and logged in users
    # @ram.cache(lambda *args: time() // 60)  # cache for one minute
    def get_latest_journalentries(self):
        """Return journal-entries posted in the last minute."""
        updates = self.context.get_journalentries()
        updates = [u for u in updates if u["timestamp"] > str(time() - 60)]
        return updates

    # TODO Refactor as this is a copy from updates.py
    def can_edit_objects(self):
        return checkPermission("cmf.ModifyPortalContent", self.context)

    def can_delete_objects(self):
        return checkPermission("zope2.DeleteObjects", self.context)

    def delete_confirmation(self):
        msg = _("Do you really want to delete this item?")
        msg = translate(msg, "elan.journal", context=self.request)
        return f"return confirm('{msg}')"
