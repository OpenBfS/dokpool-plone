from five.intid.intid import addIntIdSubscriber
from plone import api
from plone.app.upgrade.utils import loadMigrationProfile
from plone.base.utils import get_installer

import logging


log = logging.getLogger(__name__)


def to_1010(context=None):
    portal = api.portal.get()
    installer = get_installer(portal)
    if installer.is_product_installed("docpool.rei"):
        # reload workflow to change BMUV to BMUKN
        portal_setup = api.portal.get_tool("portal_setup")
        loadMigrationProfile(
            portal_setup,
            "profile-docpool.rei:default",
            steps=["workflow"],
        )


def to_1011(context=None):
    # Change history action to @@fullfull_review_history and View
    portal_setup = api.portal.get_tool("portal_setup")
    loadMigrationProfile(
        portal_setup,
        "profile-docpool.base:to_1011",
    )


def to_1012(context=None):
    # Fix regex for images and pdfs
    broken = ".*"
    fixed_pdf = ".+\.pdf$"
    fixed_image = ".+\.(png|jpg)$"
    for brain in api.content.find(portal_type="DocType"):
        obj = brain.getObject()
        if obj.pdfPattern and obj.pdfPattern == broken:
            obj.pdfPattern = fixed_pdf
            obj._p_changed = 1
            log.info("Fixed pdfPattern for %s", brain.getURL())
        if obj.imgPattern and obj.imgPattern == broken:
            obj.imgPattern = fixed_image
            obj._p_changed = 1
            log.info("Fixed imgPattern for %s", brain.getURL())

    # remove obsolete copies of transfer logs
    for brain in api.content.find(portal_type="DPDocument"):
        if hasattr((obj := brain.getObject()).aq_base, "transferLog"):
            del obj.transferLog
            obj._p_changed = 1


def to_1012_update_dp_doc_workflow(context=None):
    # Update dp_doc_workflow
    log.info("Reload dp_doc_workflow and remove Owner permissions in published state")
    portal_setup = api.portal.get_tool("portal_setup")
    loadMigrationProfile(portal_setup, "profile-docpool.base:default", steps=["workflow"])
    portal_workflow = api.portal.get_tool("portal_workflow")
    log.info("Upgrading permissions...")
    portal_workflow.updateRoleMappings()


def to_1013_fix_comments(context=None):
    for brain in api.content.find(portal_type="Discussion Item"):
        obj = brain.getObject()
        addIntIdSubscriber(obj, None)
