# -*- coding: utf-8 -*-
from docpool.config.general.base import configureGroups
from plone import api
from plone.app.contenttypes.migration.dxmigration import migrate_base_class_to_new_class
from plone.app.upgrade.utils import loadMigrationProfile
from Products.CMFPlone.utils import base_hasattr

import logging

log = logging.getLogger(__name__)


def to_1_4_00(context):
    context.runAllImportStepsFromProfile('profile-docpool.base:to_1_4_00')
    log.info('Updated registry with new js/css paths')
    portal = api.portal.get()
    configureGroups(portal)
    log.info('Configured groups')
    log.info('Start migrating DPEvent to Container class')


def make_dbevent_folderish(context):
    log.info('Start migrating DPEvent to Container class')
    context.runAllImportStepsFromProfile('profile-docpool.base:to_1_3_29')

    brains = api.content.find(portal_type='DPEvent')
    for dpevent in brains:
        dpevent_obj = dpevent.getObject()
        migrate_base_class_to_new_class(dpevent_obj, migrate_to_folderish=True)
        log.info('Migrated {}'.format(str(dpevent_obj)))


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
