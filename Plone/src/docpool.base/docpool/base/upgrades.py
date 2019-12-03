# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from docpool.config.general.base import configureGroups
from plone import api
from plone.app.contenttypes.migration.dxmigration import migrate_base_class_to_new_class
from plone.app.textfield import RichTextValue
from plone.app.upgrade.utils import loadMigrationProfile
from Products.CMFPlone.utils import base_hasattr

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