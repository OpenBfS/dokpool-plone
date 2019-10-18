# -*- coding: utf-8 -*-
from docpool.config.general.base import configureGroups
from plone import api
import logging


logger = logging.getLogger(__name__)

def to_1_3_29(context):
    context.runAllImportStepsFromProfile('profile-docpool.base:to_1_3_29')
    logger.info('Updated registry with new js/css paths')

    portal = api.portal.get()
    configureGroups(portal)
