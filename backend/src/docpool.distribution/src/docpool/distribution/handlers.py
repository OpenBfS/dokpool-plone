from logging import getLogger
from plone import api
from plone.dexterity.content import ASSIGNABLE_CACHE_KEY
from plone.distribution.core import Distribution
from Products.CMFPlone.Portal import PloneSite
from Products.ZCatalog.ProgressHandler import ZLogHandler
from zope.globalrequest import getRequest


logger = getLogger(__name__)


def pre_handler(answers: dict) -> dict:
    """Process answers."""
    return answers


def post_handler(
    distribution: Distribution, site: PloneSite, answers: dict
) -> PloneSite:
    """Run after site creation."""
    logger.info(f"{site.id}: Running {distribution.name} post_handler")

    # Invalidate behavior cache to get the correct apps
    request = getRequest()
    delattr(request, ASSIGNABLE_CACHE_KEY)

    logger.info("Reindexing a bunch of indexes")
    catalog = api.portal.get_tool("portal_catalog")
    pghandler = ZLogHandler(steps=1000)
    catalog.reindexIndex(
        [
            "created",
            "modified",
            "mdate",
            "apps_supported",
            "changed",
            "scenarios",
            "category",
        ],
        REQUEST=None,
        pghandler=pghandler,
    )
    return site
