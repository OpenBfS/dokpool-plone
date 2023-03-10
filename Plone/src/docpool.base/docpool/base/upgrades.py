# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import base_hasattr
from Products.CMFPlone.utils import get_installer
from Products.CMFPlone.utils import safe_unicode
from bs4 import BeautifulSoup
from collections import defaultdict
from docpool.base.content.documentpool import DocumentPool
from docpool.base.content.documentpool import docPoolModified
from docpool.config.general.base import configureGroups
from docpool.config.utils import set_local_roles
from docpool.event.utils import get_global_scenario_selection
from docpool.rei.vocabularies import AUTHORITIES
from plone import api
from plone.app.contenttypes.migration.dxmigration import migrate_base_class_to_new_class
from plone.app.textfield import RichTextValue
from plone.app.theming.utils import applyTheme
from plone.app.theming.utils import getTheme
from plone.app.upgrade.utils import loadMigrationProfile
from plone.dexterity.interfaces import IDexterityFTI
from zope.component import queryUtility

import json
import logging

log = logging.getLogger(__name__)


def to_1_4_00(context):
    context.runAllImportStepsFromProfile('profile-docpool.base:to_1_4_00')
    log.info('Updated registry with new js/css paths')
    portal = api.portal.get()
    configureGroups(portal)
    log.info('Configured groups')


def make_dbevent_folderish(context):
    log.info('Start migrating DPEvent to Container class')
    # work around issue where the catalog already thinks dpevent is folderish
    # by getting the parents and accessing dp from there.
    brains = api.content.find(portal_type='DPEvents')
    log.info('Found DPEvent brains: {}'.format(str(len(brains))))
    for brain in brains:
        dpevents = brain.getObject()
        for obj in dpevents.contentValues():
            if obj.portal_type == 'DPEvent':
                log.info('Try to migrate {}'.format(obj.absolute_url()))
                migrate_base_class_to_new_class(obj, migrate_to_folderish=True)
                log.info('Migrated {}'.format(str(obj)))


def update_dbevent_schema(context=None):
    portal_setup = api.portal.get_tool('portal_setup')

    # add role EventEditor and and
    # add permission docpool.event.ManageDPEvents
    # reload workflow to allow Editing and adding Events.
    loadMigrationProfile(
        portal_setup,
        'profile-docpool.event:default',
        steps=['rolemap', 'workflow'],
        )

    # Adapt existing events to changes in event schema
    for brain in api.content.find(portal_type='DPEvent'):
        obj = brain.getObject()

        # Set EventType (#2573)
        if base_hasattr(obj.aq_base, 'Exercise'):
            if obj.Exercise:
                obj.EventType = 'exercise'
            else:
                obj.EventType = 'event'
            del obj.Exercise

        # Events need a mode (#2573)
        if not getattr(obj.aq_base, 'OperationMode'):
            obj.OperationMode = 'routine'
        log.info('Updated {}'.format(obj.absolute_url()))

        # Update indexed permission after EventEditor was added
        obj.reindexObjectSecurity()


def create_json_changelog(context=None):
    for brain in api.content.find(portal_type='DPEvent'):
        obj = brain.getObject()
        result = []
        if obj.changelog and isinstance(obj.changelog, RichTextValue):
            soup = BeautifulSoup(obj.changelog.output, 'lxml')
            head = soup.select('th')
            for tr in soup.select('tr'):
                entry = {}
                for index, td in enumerate(tr.select('td')):
                    entry[head[index].text.strip()] = td.text.strip()
                if '(' in entry.get('Date', ''):
                    date, user = entry['Date'].split(u'(', 1)
                    entry[u'Date'] = date
                    entry[u'User'] = user[:-1]
                if entry:
                    result.append(entry)
            log.info(u'Migrated changelog to json for {}'.format(
                obj.absolute_url()))
            obj.changelog = json.dumps(result)


def to_1000(context=None):
    portal_setup = api.portal.get_tool('portal_setup')
    loadMigrationProfile(portal_setup, 'profile-docpool.base:to_1000')


def reindex_catpath(context=None):
    """Reindex dpdocs with updated index ."""
    log.info(u'Reindexing DPDocuments.')
    brains = api.content.find(portal_type='DPDocument')
    log.info(u'Found {0} DPDocument to reindex'.format(len(brains)))
    for brain in brains:
        obj = brain.getObject()
        obj.reindexObject(idxs=['cat_path'])
    log.info('Done.')


def update_doksys_collections(context=None):
    """Remove existing collections and replace with new ones.
    See https://redmine-koala.bfs.de/issues/3165
    """
    from docpool.doksys.setuphandlers import create_today_collection
    from docpool.doksys.setuphandlers import create_since_yesterday_collection
    portal = api.portal.get()
    if 'searches' not in portal.keys():
        log.info(u'Missing folder /searches. doksys may not be installed.')
        return
    searches = portal['searches']
    if 'today' in searches or 'yesterday' in searches:
        log.info(u'Skip updating doksys-collections. Is already up to date.')
        return
    api.content.delete(searches['last24h'])
    create_today_collection(portal)
    create_since_yesterday_collection(portal)
    searches.moveObjectsToTop(['today', 'yesterday'])
    log.info(u'Updated templates for doksys-collections.')

    for brain in api.content.find(portal_type='DocumentPool'):
        docpool = brain.getObject()
        if 'doksys' not in docpool.supportedApps:
            log.info(u'Skip docpool %s because it has no doksys.', docpool.id)
            continue
        dp_searches = docpool['searches']
        api.content.delete(dp_searches['last24h'])
        api.content.copy(source=searches['today'], target=dp_searches)
        api.content.copy(source=searches['yesterday'], target=dp_searches)
        dp_searches.moveObjectsToTop(['today', 'yesterday'])
        log.info(u'Updated doksys-collections for {}'.format(docpool.id))


def install_rei(context=None):
    portal = api.portal.get()
    installer = get_installer(portal)
    if not installer.is_product_installed('docpool.rei'):
        installer.install_product('docpool.rei')
        log.info(u'docpool.rei installed')
    bund = portal.get('bund')
    if not bund or not isinstance(bund, DocumentPool):
        log.info(u'Aborting. No docpool "bund" exists!')
        return
    if 'rei' in bund.supportedApps:
        log.info(u'REI is already enabled for bund.')
        return

    log.info(u'Enabling rei for bund...')
    bund.supportedApps.append('rei')
    # trigger content-creation
    docPoolModified(bund)
    container = bund['config']['dtypes']
    if 'reireport' in container:
        log.info(u'DType reireport already exists!')
    reireport = portal['config']['dtypes']['reireport']
    api.content.copy(source=reireport, target=container)
    log.info(u'Copied dtype reireport to bund')


def to_1001(context=None):
    portal_setup = api.portal.get_tool('portal_setup')
    log.info('Importing 1001 upgrades')
    loadMigrationProfile(portal_setup, 'profile-docpool.base:to_1001')


def change_theme(context=None):
    log.info('Enabling the new webpack theme')
    webpack_theme = getTheme("docpooltheme")
    applyTheme(webpack_theme)


def to_1002(context=None):
    log.info('Importing 1002 upgrades')
    portal_setup = api.portal.get_tool('portal_setup')

    # allow journal in ESD to fix archiving events
    fti = queryUtility(IDexterityFTI, name='ELANCurrentSituation')
    if 'Journal' not in fti.allowed_content_types:
        allowed = list(fti.allowed_content_types)
        allowed.append('Journal')
        fti.manage_changeProperties(allowed_content_types=tuple(allowed))
        log.info('Allowed Journal in ELANCurrentSituation')


    # remove Roles JournalXX Editor
    portal = api.portal.get()
    roles = list(portal.__ac_roles__)
    for index in range(1, 11):
        role = 'Journal{} Editor'.format(index)
        try:
            roles.remove(role)
            log.info('Removed obsolete role {}'.format(role))
        except:
            pass
    portal.__ac_roles__ = tuple(roles)

    # Set workflow for journals and add roles
    loadMigrationProfile(
        portal_setup,
        'profile-elan.journal:default',
        steps=['rolemap', 'workflow'],
        )
    wtool = api.portal.get_tool('portal_workflow')
    wtool.updateRoleMappings()
    # TODO: THIS IS NOT ENOUGH YET!
    log.info('Set workflow for Journals and added roles JournalEditor and JournalReader')

    # Add Journal groups for all docpools where elan is active
    for brain in api.content.find(portal_type='DocumentPool'):
        docpool = brain.getObject()
        prefix = docpool.prefix or docpool.getId()
        title = docpool.Title()
        if 'elan' not in docpool.allSupportedApps():
            log.info(u'Skipping docpool {} because elan is not enabled'.format(title))
            continue
        gtool = getToolByName(docpool, 'portal_groups')
        for index in range(1, 6):
            props = {
                'allowedDocTypes': [],
                'title': 'Journal {} Editors ({})'.format(index, title),
                'description': 'Users who can edit journal{} in {}.'.format(index, title),
                'dp': docpool.UID(),
            }
            gtool.addGroup("{}_Journal{}_Editors".format(prefix, index), properties=props)

        for index in range(1, 6):
            props = {
                'allowedDocTypes': [],
                'title': 'Journal {} Reader ({})'.format(index, title),
                'description': 'Users who can view journal{} in {}.'.format(index, title),
                'dp': docpool.UID(),
            }
            gtool.addGroup("{}_Journal{}_Readers".format(prefix, index), properties=props)
        log.info(u'Added Journal groups for docpool {}'.format(title))

    # set local roles for all journals in all events
    for brain in api.content.find(portal_type='Journal'):
        journal = brain.getObject()
        docpool = journal.myDocumentPool()
        prefix = docpool.prefix or docpool.getId()
        index = journal.id.split('journal')[-1]
        # Grant local role to Journal Editor Groups
        api.group.grant_roles(
            groupname='{}_Journal{}_Editors'.format(prefix, index),
            roles=['JournalEditor'],
            obj=journal,
            )
        # Grant local role to Journal Reader Groups
        api.group.grant_roles(
            groupname='{}_Journal{}_Readers'.format(prefix, index),
            roles=['JournalReader'],
            obj=journal,
            )
        # reindex security for journals
        journal.reindexObjectSecurity()
        log.info(u'Added local roles for Journal {}'.format(journal.title))


def to_1003(context=None):
    log.info('Running 1003 upgrades')
    # adapt reidoc to changes in NuclearInstallationVocabulary
    from docpool.rei.behaviors.reidoc import IREIDoc
    for brain in api.content.find(portal_type='DPDocument'):
        obj = brain.getObject()
        try:
            wrapped = IREIDoc(obj)
        except TypeError:
            log.info(u'{} is no reidoc'.format(obj.absolute_url()))
            continue
        new = []
        old = getattr(wrapped, 'NuclearInstallations', [])
        for value in old:
            new.append(str(value[:4]))
        if new:
            wrapped.NuclearInstallations = new
            log.info(u'Set NuclearInstallations for {} to {}'.format(
                obj.absolute_url(), new))


def to_1004(context=None):
    portal_setup = api.portal.get_tool('portal_setup')
    log.info('Importing 1004 upgrades')
    loadMigrationProfile(portal_setup, 'profile-docpool.base:to_1004')
    rei_reports = api.content.find(portal_type='DPDocument', dp_type='reireport')
    for brain in rei_reports:
        rei_report = brain.getObject()
        if not hasattr(rei_report, 'Authority'):
            log.error("Broken rei_report: {0}".format(str(rei_report)))
        if rei_report.Authority in AUTHORITIES.values():
            for iso_id, authority in AUTHORITIES.items():
                if authority == rei_report.Authority:
                    rei_report.Authority = iso_id
                    rei_report.reindexObject()
                    log.info("Authority {0} updated with {1}".format(rei_report, iso_id))
        else:
            log.error("Broken data")


def to_1005(context=None):
    portal_setup = api.portal.get_tool('portal_setup')
    log.info('Upgrading to 1005: reload workflows')
    loadMigrationProfile(
        portal_setup, 'profile-docpool.base:default', steps=['workflow'])
    loadMigrationProfile(
        portal_setup, 'profile-docpool.rei:default', steps=['workflow'])
    loadMigrationProfile(
        portal_setup, 'profile-elan.esd:default', steps=['workflow'])
    loadMigrationProfile(
        portal_setup, 'profile-elan.sitrep:default', steps=['workflow'])


def enable_bulk_actions(context=None):
    portal_setup = api.portal.get_tool('portal_setup')
    # add transfer action to folder_buttons
    loadMigrationProfile(
        portal_setup,
        'profile-docpool.base:default',
        steps=['actions'],
        )
    # enable docpool_collection_view_with_actions for collections
    fti = queryUtility(IDexterityFTI, name='Collection')
    view = 'docpool_collection_view_with_actions'
    if view not in fti.view_methods:
        view_methods = list(fti.view_methods)
        view_methods.append(view)
        fti.manage_changeProperties(view_methods=tuple(view_methods))
        log.info('Allowed docpool_collection_view_with_actions for Collections')


def to_1006(context=None):
    log.info('Upgrading to 1006: delete IRIXConfig')

    portal_setup = api.portal.get_tool('portal_setup')
    loadMigrationProfile(
        portal_setup, 'profile-docpool.caching:default', steps=['plone.app.registry'])
    loadMigrationProfile(
        portal_setup,
        'profile-elan.esd:default',
        steps=['content_type_registry', 'workflow']
    )

    for brain in api.content.find(portal_type='DocumentPool'):
        docpool = brain.getObject()
        try:
            api.content.delete(docpool['contentconfig']['irix'])
        except KeyError:
            pass


def to_1007(context=None):
    log.info('Upgrading to 1007: allow Text inside DokumentPool, translate actions')
    loadMigrationProfile(context, 'profile-docpool.base:to_1007')


def to_1007_move_help_pages(context=None):
    log.info('Upgrading to 1007: move help pages')

    portal = api.portal.get()
    if 'help' not in portal['contentconfig']:
        return

    help = portal['contentconfig']['help']

    for brain in api.content.find(portal_type='DocumentPool'):
        docpool = brain.getObject()
        try:
            api.content.move(docpool['contentconfig']['help'], docpool)
        except KeyError:
            api.content.copy(help, docpool)
        set_local_roles(
            docpool,
            docpool['help'],
            '{0}_ContentAdministrators',
            ['ContentAdmin']
        )

    api.content.delete(help)


def to_1007_delete_local_impressum_pages(context=None):
    log.info('Upgrading to 1007: delete local impressum pages')

    for brain in api.content.find(portal_type='DocumentPool'):
        docpool = brain.getObject()
        try:
            api.content.delete(docpool['contentconfig']['impressum'])
        except KeyError:
            pass

    portal = api.portal.get()
    if 'impressum' in portal['contentconfig']:
        api.content.move(portal['contentconfig']['impressum'], portal)


def to_1008_remove_irix(context=None):
    for brain in api.content.find(portal_type='IRIXConfig'):
        log.info(u'Deleting {}'.format(brain.getPath()))
        try:
            obj = brain.getObject()
        except Exception:
            log.info('Could not resolve {}'.format(brain.getPath()))
            continue
        api.content.delete(obj)
    portal_setup = api.portal.get_tool('portal_setup')
    loadMigrationProfile(portal_setup, 'profile-docpool.base:ticket_3954_remove_irix')


def to_1008(context=None):
    portal_setup = api.portal.get_tool('portal_setup')
    log.info('Upgrading to 1008: adding report year index')
    loadMigrationProfile(portal_setup, 'profile-docpool.base:to_1008')


def to_1008_index_report_year(context=None):
    log.info(u'Reindexing rei reports.')
    brains = api.content.find(portal_type='DPDocument', dp_type='reireport')
    log.info(u'Found {0} rei reports to reindex'.format(len(brains)))
    for brain in brains:
        obj = brain.getObject()
        obj.reindexObject(idxs=['report_year'])
    log.info('Done.')


def to_1008_fix_unicode_indexes(context=None):
    # Rebuild indexes with unicode values that fail in py2. See #4084
    catalog = api.portal.get_tool('portal_catalog')
    log.info('Rebuild index Origins ...')
    catalog.manage_clearIndex(ids=['Origins'])
    catalog.manage_reindexIndex(ids=['Origins'])
    log.info('Rebuild index category ...')
    catalog.manage_clearIndex(ids=['category'])
    catalog.manage_reindexIndex(ids=['category'])
    log.info('Done.')


def to_1008_install_z3ctable(context=None):
    portal = api.portal.get()
    installer = get_installer(portal)
    if not installer.is_product_installed('collective.eeafaceted.z3ctable'):
        installer.install_product('collective.eeafaceted.z3ctable')
        log.info(u'collective.eeafaceted.z3ctable installed')


def to_1009_capitalise_event_types(context=None):
    log.info(u'Capitalising event types.')
    events = [b.getObject() for b in api.content.find(portal_type='DPEvent')]

    TYPE_MAP = {
        None: None,
        'exercise': 'Exercise',
        'event': 'Emergency',
        'test': 'Test',
    }
    for event in events:
        event.EventType = TYPE_MAP.get(event.EventType, event.EventType)

def to_1009(context=None):
    portal_setup = api.portal.get_tool('portal_setup')
    loadMigrationProfile(portal_setup, 'profile-docpool.base:to_1009')


def to_1009_update_dp_folder_workflow(context=None):
    log.info('Upgrading to 1009: Reload dp_folder_workflow')
    portal_setup = api.portal.get_tool('portal_setup')
    loadMigrationProfile(portal_setup, 'profile-docpool.base:default', steps=['workflow', 'actions'])
    portal_workflow = api.portal.get_tool("portal_workflow")
    log.info('Upgrading permissions')
    portal_workflow.updateRoleMappings()


def to_1009_archive_closed_events(context=None):
    portal_setup = api.portal.get_tool('portal_setup')
    # Add DPEvent to allowed allowed_content_types of ELANArchive
    loadMigrationProfile(portal_setup, 'profile-elan.esd:default', steps=['typeinfo'])

    # move closed events to theit respective ELANArchive
    EVENT_MAPPING = {
        "bund": {
            "japan-strong-earthquake": "japan-strong-earthquake_05-04-2022-21-41",
            "uebung-core-2021": "uebung-core-2021_31-12-2021-12-17",
            "schlungsereignis-02-12.2021": "schlungsereignis-02-12-2021_31-12-2021-12-08",
            "voruebungen-zur-core21": "voruebungen-zur-core21",
            "stoerfall-im-kernkraftwerk-nowhere-belgien-region-krewinkel-afst": "stoerfall-im-kernkraftwerk-nowhere-belgien-region",
            "imis-uebung-2021": "imis-uebung-2021_12-10-2021-09-13",
            "moduluebung-21-05.2021": "moduluebung-21-05-2021_22-05-2021-13-05",
            "unfall-im-kernkraftwerk-emsland": "unfall-im-kernkraftwerk-emsland_26-01-2021-08-38",
            "site-area-emergency-olkiluoto-2-finnland": "site-area-emergency-olkiluoto-2-finnland_12-12",
            "08-12-20-techniktest-virtuelles-lagezentrum": "08-12-20-techniktest-virtuelles-lagezentrum_12-12",
            "moduluebungen-ab-oktober-2020": "moduluebungen-ab-oktober-2020_12-12-2020-18-40",
            "moduluebungen-zur-lagebilderstellung-ab-juli-2020": "imis-uebung-berlin-brandenburg-2020-10",
            "nachweis-von-sehr-geringen-spuren-von-kuenstlichen-radionukliden-in-schweden-und-finnland-23-06.20": "sehr-geringe-spuren-von-kuenstlichen-radionukliden",
            "test-zur-lagebild-erstellung-maerz-april-2020": "test-zur-lagebild-erstellung-maerz-april-2020_14",
            "waldbraende-bei-tschernobyl-04-04-2020": "waldbraende-bei-tschernobyl-04-04-2020_21-06-2020",
            "testlauf-rlz-bfs-am-18-3.20": "testlauf-rlz-bfs-am-18-3-20_25-03-2020-13-01",
            "uebung-forschungsreaktor-garching": "uebung-forschungsreaktor-garching_06-02-2020-09-15",
            "gnu-stylos": "gnu-stylos_28-11-2019-15-50",
            "testintensivbetrieb-imis3-201910": "testintensivbetrieb-imis3-201910_15-10-2019-16-40",
        },
        "baden-wuerttemberg": {
            "gnu-stylos": "gnu-stylos_13-01-2020-17-08",
        },
        "berlin": {
            "japan-strong-earthquake": "japan-strong-earthquake_08-04-2022-14-47",
            "imis-uebung-2021": "imis-uebung-2021_24-02-2022-16-04",
            "imis-uebung-berlin-brandenburg-202010": "imis-uebung-berlin-brandenburg-202010_27-11-2020",
        },
        "brandenburg": {
            "exercise-imis-uebung-2021": "exercise-imis-uebung-2021_17-12-2021-11-47",
            "imis-uebung-berlin-brandenburg-202010": "imis-uebung-berlin-brandenburg-202010_27-11-2020",
        },
        "schleswig-holstein": {
            "test-odl": None,  # ???
        },
        "thueringen": {
            "informationen-zur-radiologischen-lage-in-der-ukraine": "informationen-zur-radiologischen-lage-in-der"
        }
    }

    for brain in api.content.find(portal_type="DPEvent"):
        obj = brain.getObject()
        if obj.Status != 'closed':
            continue
        if obj.__parent__.portal_type == "ELANArchive":
            continue

        current_docpool = None
        for item in obj.aq_chain:
            if item.portal_type == "DocumentPool":
                current_docpool = item
                break
        if not current_docpool:
            raise RuntimeError(u"No docpool found for {}".format(obj.absolute_url()))

        # Find the right ELANArchive using a manual mapping
        archive = None
        archives = api.content.find(context=current_docpool, portal_type="ELANArchive")
        mapping = EVENT_MAPPING.get(current_docpool.id, {})
        archive_id = mapping.get(obj.id)
        if archive_id and archive_id in [brain.id for brain in archives]:
            for brain in archives:
                if brain.id == archive_id:
                    archive = brain.getObject()
                    break

        if not archive:
            log.warning(u"No ELANArchive found for {}".format(obj.absolute_url()))
            continue

        old_url = obj.absolute_url()
        archived_event = api.content.move(obj, target=archive)
        archived_event.reindexObject()
        log.info(u"Moved Event {} ({}) to {} as {}".format(obj.title, old_url, archive.title, archived_event.absolute_url()))

        # remove old archived/copied journals. they are now inside the event
        esd = api.content.find(context=archive, portal_type="ELANCurrentSituation", sort_on="path")
        # there can only be one esd
        assert(len(esd)==1)
        esd = esd[0].getObject()

        new_journal_brains = api.content.find(context=archived_event, portal_type="Journal", sort_on="path")
        old_journal_brains = api.content.find(context=esd, portal_type="Journal", sort_on="path")
        if old_journal_brains and len(old_journal_brains) == len(new_journal_brains):
            for brain in old_journal_brains:
                api.content.delete(brain.getObject())
        elif len(old_journal_brains) > len(new_journal_brains):
            log.info("Inconsitent number of journals in esd %s", esd.absolute_url())
            log.info("Old archived journals: %s", len(old_journal_brains))
            log.info("New archived journals: %s", len(new_journal_brains))
            # We keep the old ones and move them to archived_event
            for brain in new_journal_brains:
                api.content.delete(brain.getObject())
            for brain in old_journal_brains:
                api.content.move(brain.getObject(), target=archived_event)

        elif len(old_journal_brains) < len(new_journal_brains):
            log.info("Inconsitent number of journals in esd %s", esd.absolute_url())
            log.info("Old archived journals: %s", len(old_journal_brains))
            log.info("New archived journals: %s", len(new_journal_brains))
            # We keep the new ones and delete the old ones
            for brain in old_journal_brains:
                api.content.delete(brain.getObject())

    # check for consistency
    for brain in api.content.find(portal_type="DPEvent", sort_on="path"):
        obj = brain.getObject()
        parent = obj.__parent__
        if obj.Status == "closed" and parent.portal_type != "ELANArchive":
            log.warning(u"Archived %s Event in wrong container: %r", obj.absolute_url(), parent)

        if obj.Status != "closed" and parent.portal_type != "DPEvents":
            log.warning(u"Unarchived Event %s in wrong container: %r", obj.absolute_url(), parent)

    for brain in api.content.find(portal_type="Journal", sort_on="path"):
        obj = brain.getObject()
        parent = obj.__parent__
        if parent.portal_type != "DPEvent":
            log.warning(u"Journal %s in wrong container: %r", obj.absolute_url(), parent)

    for brain in api.content.find(portal_type="ELANArchive", sort_on="path"):
        obj = brain.getObject()
        events = api.content.find(context=obj, portal_type="DPEvent")
        if len(events) != 1:
            log.warning(u"%s DPEvent in Archive %s", len(events), obj.absolute_url())

    log.info(u"Archived all closed Events")


def to_1010(context=None):
    portal_setup = api.portal.get_tool('portal_setup')
    loadMigrationProfile(portal_setup, 'profile-docpool.base:to_1010')


def to_1011_update_rolemappings(context=None):
    """to_1009_update_dp_folder_workflow previously only reindexed security
    It needs to update the rolemappings to have the managed permission 'Delete objects'
    set on the objects. See #4560
    """
    portal_workflow = api.portal.get_tool("portal_workflow")
    log.info('Upgrading permissions')
    portal_workflow.updateRoleMappings()


def to_1011_uuids_for_event_selection(context=None):
    scen_map = defaultdict(list)
    for scen in api.content.find(portal_type='DPEvent'):
        scen_map[scen.getId].append(scen.UID)

    global_scenarios = get_global_scenario_selection()
    from pprint import pprint
    pprint(global_scenarios)
    for scen_id, status in global_scenarios.items():
        global_scenarios.update((scen_uid, status) for scen_uid in scen_map[scen_id])
        del global_scenarios[scen_id]
    pprint(global_scenarios)

    for user in api.user.get_users():
        selections = user.getProperty('scenarios', [])
        new_selections = []
        for line in selections:
            scen, selected = line.strip().rsplit(':', 1)
            new_selections.extend(
                '{}:{}'.format(scen_uid, selected) for scen_uid in scen_map[scen]
            )
        user.setMemberProperties({'scenarios': new_selections})
