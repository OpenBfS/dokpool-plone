from plone import api
from plone.app.upgrade.utils import loadMigrationProfile

import logging


log = logging.getLogger(__name__)


def to_1010(context=None):
    portal_setup = api.portal.get_tool("portal_setup")

    # reload workflow to change BMUV to BMUKN
    loadMigrationProfile(
        portal_setup,
        "profile-docpool.rei:default",
        steps=["workflow"],
    )
