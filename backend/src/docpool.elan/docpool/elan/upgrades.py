from plone import api
from plone.app.upgrade.utils import loadMigrationProfile

import logging


log = logging.getLogger(__name__)


def to_1000(context=None):
    portal_setup = api.portal.get_tool("portal_setup")
    loadMigrationProfile(portal_setup, "profile-docpool.elan:to_1000")
