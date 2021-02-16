# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import base_hasattr
from Products.CMFPlone.utils import get_installer
from bs4 import BeautifulSoup
from docpool.base.content.documentpool import DocumentPool
from docpool.base.content.documentpool import docPoolModified
from docpool.config.general.base import configureGroups
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
