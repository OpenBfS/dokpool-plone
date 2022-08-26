from elan.journal import _
from elan.journal.browser.view import View
from elan.journal.config import BATCH_SIZE
from elan.journal.config import ORPHAN
from plone import api
from plone.batching import Batch
from zope.i18n import translate
from zope.security import checkPermission


class Update(View):

    """View to add entries to a Journal."""

    @property
    def batch(self):
        """Encapsulate sequence in batches of size."""
        return Batch(self.updates(), BATCH_SIZE, self.start, orphan=ORPHAN)

    def can_edit_objects(self):
        return checkPermission("cmf.ModifyPortalContent", self.context)

    def can_delete_objects(self):
        return checkPermission("zope2.DeleteObjects", self.context)

    def delete_confirmation(self):
        msg = _("Do you really want to delete this item?")
        msg = translate(msg, "elan.journal", context=self.request)
        return f"return confirm('{msg}')"

    @property
    def automatic_updates_enabled(self):
        """Check if the Livelog must be updated automatically.
        Automatic updates should be enabled on first page of batch.
        """
        enabled = super().automatic_updates_enabled
        return enabled and self.start == 0

    def __call__(self):
        if not self.context.can_add_journalentries():
            return self.request.response.redirect(self.context.absolute_url())
        self.start = int(self.request.get("b_start", 0))
        if self.start != 0:
            msg = _(
                "You must be on the first page of the batch to add journal entries."
            )
            api.portal.show_message(msg, self.request, type="info")
        return self.index()
