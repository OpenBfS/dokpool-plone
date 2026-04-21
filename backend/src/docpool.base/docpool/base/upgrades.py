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
    portal_setup = api.portal.get_tool("portal_setup")
    loadMigrationProfile(portal_setup, "profile-docpool.base:to_1013")


def to_1013_update_dp_doc_workflow(context=None):
    log.info("Reload dp_doc_workflow")
    portal_setup = api.portal.get_tool("portal_setup")
    loadMigrationProfile(portal_setup, "profile-docpool.base:default", steps=["workflow"])


def to_1014_single_scenario_per_dpdocument(context=None):
    log.info("Turn DPDocument's scenarios attribute into single-valued scenario attribute.")
    multiple = 0
    for brain in api.content.find(portal_type="DPDocument"):
        try:
            scns = (obj := brain.getObject()).aq_base.__getattribute__("scenarios")
        except AttributeError:
            continue
        if len(scns) > 1:
            multiple += 1
            scn_lines = [f"    {s} {'/'.join(api.content.get(UID=s).getPhysicalPath())}" for s in scns]
            log.warn(f"Multiple scenarios for {brain.getPath()}:\n{'\n'.join(scn_lines)}")
            continue
        obj.scenario = scns[0] if scns else None
        del obj.scenarios
        obj._p_changed = 1
        obj.reindexObject(idxs=["scenario"])
    if multiple:
        log.warn(f"Need manual clean-up: {multiple} documents assigned to multiple scenarios.")


def to_1014_update_elan_scenario_index(context=None):
    log.info("Update ELAN scenario index")
    portal_setup = api.portal.get_tool("portal_setup")
    loadMigrationProfile(portal_setup, "profile-docpool.elan:to_1001")
