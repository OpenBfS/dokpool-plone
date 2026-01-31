from Acquisition import aq_get
from logging import getLogger
from plone import api
from plone.dexterity.content import ASSIGNABLE_CACHE_KEY
from plone.distribution.core import Distribution
from Products.CMFPlone.Portal import PloneSite
from Products.ZCatalog.ProgressHandler import ZLogHandler
from zope.globalrequest import getRequest
from zope.lifecycleevent import modified

import os


logger = getLogger(__name__)

from eea.facetednavigation.layout.interfaces import IFacetedLayout
from Products.GenericSetup.context import SnapshotImportContext
from Products.GenericSetup.interfaces import IBody
from zope.component._api import queryMultiAdapter


def pre_handler(answers: dict) -> dict:
    """Process answers."""
    return answers


def post_handler(distribution: Distribution, site: PloneSite, answers: dict) -> PloneSite:
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

    # Configure EEA faceted navigation
    import_file_path = os.path.join(os.path.dirname(__file__), "profiles/default/rei_search.xml")
    search_folder = api.content.get(path="/Plone/bund/rei-bericht-suche")
    search_collection = search_folder["rei-bericht-suche"]
    search_folder.setDefaultPage("rei-bericht-suche")
    # Collection already exists, populate query
    query = [
        {"i": "dp_type", "o": "plone.app.querystring.operation.selection.is", "v": ["reireport"]},
        {
            "i": "review_state",
            "o": "plone.app.querystring.operation.selection.any",
            "v": ["pending_bfs", "pending_bmu", "pending_authority", "published", "private"],
        },
    ]
    search_collection.query = query
    _configure_faceted_view(search_collection, import_file_path, "faceted-table-items")
    modified(search_collection)

    portal_workflow = api.portal.get_tool("portal_workflow")
    portal_workflow.updateRoleMappings()
    return site


def _configure_faceted_view(obj, import_file_path, layout_id):
    logger.info(
        "Loading configuration {} for faceted view on {}".format(
            import_file_path, "/".join(obj.getPhysicalPath())
        )
    )
    subtyper = api.content.get_view("faceted_subtyper", obj, aq_get(obj, "REQUEST"))
    subtyper.enable()
    with open(import_file_path) as import_file:
        xml = import_file.read()
        environ = SnapshotImportContext(obj, "utf-8")
        importer = queryMultiAdapter((obj, environ), IBody)
        importer.body = xml
    IFacetedLayout(obj).update_layout(layout_id)
