# -*- coding: utf-8 -*-
from docpool.config.general.base import configureGroups
from plone import api
import logging
import plone.api as api
from plone.app.contenttypes.migration.dxmigration import migrate_base_class_to_new_class

logger = logging.getLogger(__name__)


def to_1_4_00(context):
    context.runAllImportStepsFromProfile('profile-docpool.base:to_1_4_00')
    logger.info('Updated registry with new js/css paths')
    portal = api.portal.get()
    configureGroups(portal)
    logger.info('Configured groups')
    logger.info('Start migrating DPEvent to Container class')
    brains = api.content.find(portal_type='DPEvent')
    for dpevent in brains:
        dpevent_obj = dpevent.getObject()
        migrate_base_class_to_new_class(dpevent_obj,migrate_to_folderish=True)
        logger.info('Migrated {}'.format(str(dpevent_obj)))
