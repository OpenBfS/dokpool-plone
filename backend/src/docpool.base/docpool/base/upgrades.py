from docpool.base.behaviors.transferable import ITransferable
from docpool.base.content.contentbase import IContentBase
from docpool.base.content.documentpool import APPLICATIONS_KEY
from docpool.base.content.simplefolder import ISimpleFolder
from docpool.base.setuphandlers import create_session_stuff
from docpool.base.utils import getDocumentPoolSite
from docpool.config.general.elan import DOCTYPES
from five.intid.intid import addIntIdSubscriber
from plone import api
from plone.app.upgrade.utils import loadMigrationProfile
from plone.base.utils import get_installer
from plone.dexterity.interfaces import IDexterityFTI
from Products.CMFPlone.controlpanel.events import handleConfigurationChangedEvent
from Products.ZCatalog.ProgressHandler import ZLogHandler
from zc.relation.interfaces import ICatalog
from zope.annotation.interfaces import IAnnotations
from zope.component import getUtility

import logging


log = logging.getLogger(__name__)

OLD_OBJ_MAPPING = {
    "measurement_strategy": [
        "/dokpool/bund/archive/uebung-core-2021_31-12-2021-12-17/content/Transfers/dokumente-aus-ni/messstrategie",
        "/dokpool/niedersachsen/content/Groups/ni_e-ni-nlwkn/messstrategie",
        "/hamburg/content/Transfers/dokumente-aus-bund/elan-praxistag-exercise-messstrategie-zum-rlb-1-des-bundes-exercise",
        "/hessen/content/Transfers/dokumente-aus-bund/elan-praxistag-exercise-messstrategie-zum-rlb-1-des-bundes-exercise",
        "/hessen/content/Transfers/dokumente-aus-bund/uebung-messstrategie-als-anlage-zum-6-rlb-10-45-uhr-uebung",
        "/mecklenburg-vorpommern/content/Transfers/dokumente-aus-bund/elan-praxistag-exercise-messstrategie-zum-rlb-1-des-bundes-exercise",
        "/mecklenburg-vorpommern/content/Transfers/dokumente-aus-bund/uebung-messstrategie-als-anlage-zum-6-rlb-10-45-uhr-uebung",
        "/nordrhein-westfalen/content/Transfers/dokumente-aus-bund/elan-praxistag-exercise-messstrategie-zum-rlb-1-des-bundes-exercise",
        "/rheinland-pfalz/content/Transfers/dokumente-aus-bund/elan-praxistag-exercise-messstrategie-zum-rlb-1-des-bundes-exercise",
    ],
    "measurement_recommendation": [
        "/dokpool/schleswig-holstein/content/Groups/sh_e-sh-melund/kfue/automatisch/teil-g2/b71a1312-944c-4dd1-839e-0aa910aa4d69",
        "/dokpool/schleswig-holstein/archive/uebung-kkb-2023-1_22-11-2023-13-35/content/Groups/sh_e-sh-melund/6139c042-ef6f-42de-b361-487a2a15da9e/",
    ],
    "additional_event_information": [
        "/dokpool/schleswig-holstein/archive/stabstraining-umweltministerium-sh-11-03-25_30-07/content/Groups/sh_e-sh-melund/seekarte",
    ],
    "official_notification": [
        "/thueringen/content/Transfers/dokumente-aus-bund/0afd0522-1f15-429e-b377-f59cf2f93d98",
        "/thueringen/content/Transfers/dokumente-aus-bund/81eb5caf-ee00-43e6-b0d5-6702a461a8a8",
        "/thueringen/content/Transfers/dokumente-aus-bund/a68a9d8a-16ba-4b27-9523-bd0591c17d15",
        "/thueringen/content/Transfers/dokumente-aus-bund/e5c73cea-97d4-4093-8adb-ba4aa6667b2a",
        "/thueringen/content/Transfers/dokumente-aus-bund/iaea-usie-meldung-ru-event-notice-form-enf-version-1-und-2",
        "/thueringen/content/Transfers/dokumente-aus-bund/iaea-usie-meldung-ukr-event-notice-form-enf-no-273-und-274",
        "/thueringen/content/Transfers/dokumente-aus-bund/uebung-relevantes-ereignis-an-einer-kerntechnischen-referenzanlage-in-ringhals-schweden",
    ],
    "other_entry": [
        "/dokpool/niedersachsen/archive/imis-aufbauschulung-q2-2025-1_29-07-2025-12-43/content/Groups/ni_e-ni-nlwkn/einsatzkarte",
        "/dokpool/schleswig-holstein/content/Groups/sh_e-sh-melund/kfue/automatisch/teil-g3/7626f52a-5e2e-440e-8471-cda28ef25a04",
        "/uebungen/content/Groups/ueb_bfs_uebteam/drehbuch-zur-core-uebung",
        "/uebungen/content/Groups/ueb_bfs_uebteam/kurzbericht",
    ],
    "mresult_air_external_radiation": [
        "/dokpool/bund/content/Groups/bund_e-messzentrale-bfs/mobile-messungen/automatisch/91ae0e4e-f096-4c76-abe6-1e950c8c344f",
        "/dokpool/dokpool/baden-wuerttemberg/content/Transfers/dokumente-aus-bund/91ae0e4e-f096-4c76-abe6-1e950c8c344f",
        "/dokpool/dokpool/bayern/content/Transfers/dokumente-aus-bund/91ae0e4e-f096-4c76-abe6-1e950c8c344f",
    ],
    "mresult_north_and_baltic_sea": [
        "/dokpool/bund/archive/voruebung-zur-core-2024_01-10-2024-13-12/content/Groups/bund_e-messzentrale-bfs/messergebnisse-gewaesser-1-entwurf-10-00uhr",
        "/dokpool/schleswig-holstein/archive/stabstraining-umweltministerium-sh-11-03-25_30-07/content/Groups/sh_e-sh-melund/wasserproben-von-berta",
    ],
    "mresult_other_surface_waters": [
        "/dokpool/brandenburg/archive/imis-uebung-berlin-brandenburg-202010_27-11-2020/content/Groups/bb_e-lavg/gewaesser-07-10-2020-cs",
        "/dokpool/brandenburg/archive/imis-uebung-berlin-brandenburg-202010_27-11-2020/content/Groups/bb_e-lavg/gewaesser-07-10-2020-jod",
    ],
    "mresult_drinking_water": [
        "/dokpool/brandenburg/archive/imis-uebung-berlin-brandenburg-202010_27-11-2020/content/Groups/bb_landeslabor_bbb/trinkwasser-2020-10-1.07",
        "/dokpool/brandenburg/archive/imis-uebung-berlin-brandenburg-202010_27-11-2020/content/Groups/bb_landeslabor_bbb/trinkwasser-2020-10.07",
    ],
}


def _normalize_userinfo_tuple(value, obj=None):
    if value is None:
        log.info(f"Object has no value: {obj.absolute_url()}")
        return None
    # Already done - return value
    if isinstance(value, tuple) and len(value) == 3:
        return value
    if isinstance(value, str):
        # Variant 1: Name with land and group in <i>
        # 'Firstname Lastname (Bund) <i>Radiologisches Lagezentrum (Bund)</i>'
        if "<i>" in value:
            text = value.split("<i>")
            fullname = text[0].strip()
            group = text[1].split("</i>")[0]
            log.info("Variant 1: Fullname: {} Group: {} ".format(fullname, group))
            return ("", fullname, group)
        else:
            if "(" in value and ")" in value:
                split_index = value.index(")") + 1
                fullname = value[:split_index].strip()
                group = value[split_index:].strip()
                if group == "":
                    # Variant 3: Name with land NO group
                    # 'Firstname Lastname (Thüringen)'
                    log.info("Variant 3: Fullname: {}".format(fullname))
                    return ("", fullname, "")
                # Variant 2: Name with land follwed by group
                # 'Firstname Lastname (Thüringen) Transfers'
                log.info("Variant 2: Fullname: {} Group: {} ".format(fullname, group))
                return ("", fullname, group)
            # Variant 4: Only Name
            fullname = value.strip()
            log.info("Variant 4: Fullname: {} ".format(fullname))
            return ("", fullname, "")


def _upgrade_userinfo_fields(obj):
    changed = False
    for field in ("created_by", "modified_by", "transferred_by"):
        if not hasattr(obj, field):
            continue
        value = getattr(obj, field, None)
        if value is None:
            continue
        normalized = _normalize_userinfo_tuple(value, obj)
        if normalized is None or normalized == value:
            continue
        setattr(obj, field, normalized)
        changed = True
    if changed:
        obj._p_changed = 1
    return changed


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


def to_3000(context=None):
    """Upgrade existing DB to new GUI"""
    portal = api.portal.get()
    installer = get_installer(portal)
    if not installer.is_product_installed("docpool.ui"):
        installer.install_product("docpool.ui")

    catalog = api.portal.get_tool("portal_catalog")
    # the category index changes to FieldIndex
    catalog.delIndex("category")
    portal_setup = api.portal.get_tool("portal_setup")
    loadMigrationProfile(
        portal_setup,
        "profile-docpool.base:to_3000",
    )
    create_session_stuff(portal)

    enable_elan_for_all_docpools()

    # Delete old structure first
    delete_esd_structure()

    # Drop data from relationfield to speed up stuff
    marker = object()
    for brain in api.content.find(portal_type="DocType", sort_on="path"):
        obj = brain.getObject()
        if getattr(obj.aq_base, "contentCategory", marker) is not marker:
            del obj.contentCategory

    create_doctype_structure()
    handleConfigurationChangedEvent(None)

    log.info("Indexing...")
    catalog = api.portal.get_tool("portal_catalog")
    pghandler = ZLogHandler(steps=5000)
    catalog.reindexIndex(
        [
            "dp_type",
            "apps_supported",
            "object_provides",
            "allowedRolesAndUsers",
        ],
        REQUEST=None,
        pghandler=pghandler,
    )

    log.info("Removing obsolete relations ...")
    relation_catalog = getUtility(ICatalog)
    for relationship in ["contentCategory", "dbCollections", "docTypes"]:
        query = {"from_attribute": relationship}
        for rel in [rel for rel in relation_catalog.findRelations(query)]:
            relation_catalog.unindex(rel)

    for changed_type in ["DPTransfersArea", "DPTransferFolder", "Groups", "InfoFolder", "Users", "ELANInfos"]:
        fti = getUtility(IDexterityFTI, name=changed_type)
        fti.default_view = "view"
        for brain in api.content.find(portal_type=changed_type, sort_on="path"):
            obj = brain.getObject()
            obj.setLayout("view")


def to_3000_convert_tupel(context=None):
    """Convert fields to tupel"""
    log.info("Convert userinfo")
    convert_userinfo()
    log.info("Done")


def create_doctype_structure(log_remains=False):
    rename_mapping = {}
    for item in DOCTYPES:
        for old in item["old_ids"]:
            assert old not in rename_mapping
            rename_mapping[old] = item["id"]

    for brain in api.content.find(portal_type="DocTypes", sort_on="path"):
        doctypes_container = brain.getObject()
        dp = getDocumentPoolSite(doctypes_container)

        # Move old DocTypes out of the way before moving/updating them
        if "old" not in doctypes_container:
            old_category = api.content.create(
                container=doctypes_container,
                type="DocTypeCategory",
                id="old",
                title="Old DocTypes",
            )
            old_subcategory = api.content.create(
                container=old_category,
                type="DocTypeSubCategory",
                id="old",
                title="Old DocTypes",
            )
            for obj in doctypes_container.contentValues({"portal_type": "DocType"}):
                api.content.move(source=obj, target=old_subcategory)

        # Create categories
        for info in DOCTYPES:
            if category_id := info.get("category_id"):
                if category_id in doctypes_container:
                    continue
                api.content.create(
                    container=doctypes_container,
                    type="DocTypeCategory",
                    id=category_id,
                    title=info["category"],
                )
        # Create subcategories
        for info in DOCTYPES:
            if subcategory_id := info.get("subcategory_id"):
                category_container = doctypes_container[info["category_id"]]
                if subcategory_id in category_container:
                    continue
                api.content.create(
                    container=category_container,
                    type="DocTypeSubCategory",
                    id=subcategory_id,
                    title=info["subcategory"],
                )

        # Create DocTypes
        for info in DOCTYPES:
            # Special case Bayern
            only_bayern = ["radiological_situation_report_draft", "situation_overview_draft"]
            if info["id"] in only_bayern and dp.id != "bayern":
                continue

            if dp.portal_type == "DocumentPool":
                local_behaviors = [i for i in info["behaviors"] if i in dp.supportedApps]
                # Skip DocTypes for which the DP does not have the right app
                if not local_behaviors:
                    continue
            else:
                # The portal gets all types
                local_behaviors = info["behaviors"]

            container = doctypes_container
            if category_id := info.get("category_id"):
                container = doctypes_container[info["category_id"]]
                if subcategory_id := info.get("subcategory_id"):
                    container = container[subcategory_id]
            if info["id"] in container:
                continue

            # Move and update existing doctypes
            old = doctypes_container["old"]["old"]
            for old_id in info["old_ids"]:
                if old.get(old_id) and container.get(info["id"]):
                    # A different old item with the same new id was already updated.
                    pass
                elif old_obj := old.get(old_id, None):
                    old_obj.title = info["title"]
                    old_obj.description = info["description"]
                    old_obj.local_behaviors = local_behaviors
                    api.content.move(source=old_obj, target=container, id=info["id"])

            if info["id"] not in container:
                # This is new!
                api.content.create(
                    container=container,
                    type="DocType",
                    id=info["id"],
                    title=info["title"],
                    description=info["description"],
                    local_behaviors=local_behaviors,
                )

        # Remove old doctypes that were not moved and updated, ignore links and relations
        old = doctypes_container["old"]["old"]
        for old_doctype in old.contentValues():
            if old_doctype.id in rename_mapping:
                log.debug("Deleting old DokType %s from %s", old_doctype.id, old.absolute_url())
                api.content.delete(old_doctype, check_linkintegrity=False)
        if not old.contentValues():
            api.content.delete(old, check_linkintegrity=False)

        # Log infos on remains that need to be cleaned up
        if log_remains:
            log.info("Remains in %s", dp.absolute_url())
            content_area = dp.get("content", None)
            archive_area = dp.get("archive", None)
            for old_id in old.keys():
                if old_id in rename_mapping:
                    continue
                old_obj = old[old_id]
                count_content = 0
                count_archive = 0
                if content_area:
                    count_content = len(
                        api.content.find(context=content_area, portal_type="DPDocument", dp_type=old_id)
                    )
                if archive_area:
                    count_archive = len(
                        api.content.find(context=archive_area, portal_type="DPDocument", dp_type=old_id)
                    )
                if count_content or count_archive:
                    log.info(
                        f"{old_obj.id} ({old_obj.title}): {count_content + count_archive} ({count_archive} archived)"
                    )
                else:
                    log.debug(f"{old_obj.id} ({old_obj.title})")

        # Delete all remaining old types after logging
        api.content.delete(doctypes_container["old"], check_linkintegrity=False)

    # Purge ram cache
    handleConfigurationChangedEvent(None)

    # Change all existing DPDocuments
    log.info("Updating all DPDocuments ...")
    for brain in api.content.find(portal_type="DPDocument", sort_on="path"):
        obj = brain.getObject()
        if obj.docType in rename_mapping:
            obj.docType = rename_mapping[obj.docType]
            # Update local_behaviors to fit to doctype
            # This is relevant when old obj with app 1 and doctype with app 1 changed to doctype with app 2
            doctype_obj = obj.docTypeObj()
            if not doctype_obj:
                log.info("Entry without doctype: %s", obj.absolute_url())
            elif doctype_obj and not set(doctype_obj.local_behaviors).intersection(set(obj.local_behaviors)):
                log.info(
                    "Changing local_behaviors from %s to %s for %s: %s",
                    obj.local_behaviors,
                    doctype_obj.local_behaviors,
                    obj.docType,
                    obj.absolute_url(),
                )
                obj.local_behaviors = [i for i in doctype_obj.local_behaviors if i in dp.supportedApps]
            obj.reindexObject(idxs=["category", "subcategory", "dp_type", "apps_supported"])

    # Change special cases for existing DPDocuments
    for new_doctype, paths in OLD_OBJ_MAPPING.items():
        for path in paths:
            if obj := api.content.get(path=path):
                log.info("Changing from %s to %s : %s", obj.docType, new_doctype, obj.absolute_url())
                obj.docType = new_doctype
                obj.reindexObject(idxs=["category", "subcategory", "dp_type", "apps_supported"])

    # Change all existing groups
    for group in api.group.get_groups():
        if allowed_types := group.getProperty("allowedDocTypes", []):
            new_allowed_types = list(set([rename_mapping[i] for i in allowed_types if i in rename_mapping]))
            group.setGroupProperties({"allowedDocTypes": new_allowed_types})
            log.info("Updated group %s", group.id)

    # Change allowed types for some folder types
    log.info("Updating all folders ...s")
    for brain in api.content.find(object_provides=ISimpleFolder.__identifier__):
        obj = brain.getObject()
        if allowed_types := obj.allowedDocTypes:
            new_allowed_types = [rename_mapping[i] for i in allowed_types if i in rename_mapping]
            obj.allowedDocTypes = list(set(new_allowed_types))
    for brain in api.content.find(portal_type="CollaborationFolder"):
        obj = brain.getObject()
        if allowed_types := obj.allowedPartnerDocTypes:
            new_allowed_types = [rename_mapping[i] for i in allowed_types if i in rename_mapping]
            obj.allowedPartnerDocTypes = list(set(new_allowed_types))

    # Handle special cases (Ukraine-related sitreps)
    for brain in api.content.find(portal_type="DocumentPool", sort_on="path"):
        pool = brain.getObject()
        content_area = pool["content"]
        event_uids = [
            i.UID
            for i in api.content.find(context=pool, portal_type="DPEvent", sort_on="path", Title="ukraine")
        ]
        for brain in api.content.find(
            context=content_area,
            portal_type="DPDocument",
            scenario=event_uids,
            dp_type="radiological_situation_report",
            sort_on="path",
        ):
            obj = brain.getObject()
            log.info("Change %s to situation_overview (%s)", obj.docType, obj.absolute_url())
            obj.docType = "situation_overview"
            obj.reindexObject(idxs=["category", "subcategory", "dp_type"])

    for brain in api.content.find(portal_type="ELANArchive", sort_on="path", Title="ukraine"):
        archive = brain.getObject()
        for brain in api.content.find(
            context=archive, portal_type="DPDocument", dp_type="radiological_situation_report", sort_on="path"
        ):
            obj = brain.getObject()
            log.info("Change %s to situation_overview (%s)", obj.docType, obj.absolute_url())
            obj.docType = "situation_overview"
            obj.reindexObject(idxs=["category", "subcategory", "dp_type"])


def delete_esd_structure(context=None):
    # Delete old esd structure and types
    to_delete = [
        "Dashboard",
        "DashboardsConfig",
        "DashboardCollection",
        "ELANCurrentSituation",
        "ELANDocCollection",
        "ELANSection",
    ]
    for brain in api.content.find(portal_type="ELANCurrentSituation", sort_on="path"):
        obj = brain.getObject()
        api.content.delete(obj, check_linkintegrity=False)

    for portal_type in to_delete:
        for brain in api.content.find(portal_type=portal_type, sort_on="path"):
            obj = brain.getObject()
            api.content.delete(obj, check_linkintegrity=False)
    portal_types = api.portal.get_tool("portal_types")
    for portal_type in to_delete:
        if portal_type in portal_types:
            portal_types.manage_delObjects(portal_type)


def enable_elan_for_all_docpools():
    # Enable ELAN for Bremen, Hamburg, Mecklenburg-Vorpommern, Sachsen-Anhalt (#6380)
    from docpool.config.local.elan import createBasicPortalStructure
    from docpool.config.local.elan import createContentConfig
    from docpool.config.local.elan import createELANGroups
    from docpool.config.local.elan import createELANUsers
    from docpool.config.local.elan import setELANLocalRoles
    from Products.CMFPlone.utils import log_exc
    from zExceptions import BadRequest

    for brain in api.content.find(portal_type="DocumentPool", sort_on="path"):
        obj = brain.getObject()
        if "elan" not in obj.supportedApps:
            log.info("Enabling elan for %s", obj.id)
            obj.supportedApps.append("elan")
            # Trigger content-creation with the default methods to prevent multiple reindexing of the whole portal
            annotations = IAnnotations(obj)
            annotations[APPLICATIONS_KEY].append("elan")
            fresh = True
            createBasicPortalStructure(obj, fresh)
            createContentConfig(obj, fresh)
            placeful_wf = api.portal.get_tool("portal_placeful_workflow")
            archive = obj.archive
            try:
                archive.manage_addProduct["CMFPlacefulWorkflow"].manage_addWorkflowPolicyConfig()
            except BadRequest as e:
                log_exc(e)
            config = placeful_wf.getWorkflowPolicyConfig(archive)
            placefulWfName = "elan-archive"
            config.setPolicyIn(policy=placefulWfName, update_security=False)
            config.setPolicyBelow(policy=placefulWfName, update_security=False)
            createELANUsers(obj)
            createELANGroups(obj)
            setELANLocalRoles(obj)


def convert_userinfo(context=None):
    updated = 0
    checked = 0
    seen = set()

    all_brains = api.content.find(object_provides=(ITransferable.__identifier__, IContentBase.__identifier__))
    for brain in all_brains:
        obj = brain.getObject()
        key = brain.UID or brain.getPath()
        seen.add(key)
        checked += 1
        if _upgrade_userinfo_fields(obj):
            updated += 1

    log.info("Converted userinfo fields to tuples: updated %s of %s objects", updated, checked)
