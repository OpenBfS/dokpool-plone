from docpool.base.config import PENDING_STATES
from docpool.ui.browser.listing import Listing
from logging import getLogger
from plone import api


logger = getLogger(__name__)


class Tasks(Listing):
    """Listing of pending entries that the current user can publish."""

    filters = [
        "entries",
        "date",
        "entrytype",
        "group",
        "text",
    ]

    def update(self):
        self.base_query["review_state"] = PENDING_STATES
        self.query["review_state"] = PENDING_STATES

    def include_brain(self, brain):
        # TODO: Allow listing_item to return None to drop items from list if possible
        # TODO: Then delegate that filter to listing_item
        obj = brain.getObject()
        portal_workflow = api.portal.get_tool("portal_workflow")
        if not portal_workflow.getTransitionsFor(obj):
            return False
        return True
