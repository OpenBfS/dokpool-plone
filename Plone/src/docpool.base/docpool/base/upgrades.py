# -*- coding: utf-8 -*-

from plone import api
from plone.app.upgrade.utils import loadMigrationProfile
from plone.uuid.interfaces import IUUID
from Products.CMFCore.utils import getToolByName
from zope.lifecycleevent import modified

import logging
import six


logger = logging.getLogger(__name__)

def to_1_3_29(context):
    context.runAllImportStepsFromProfile('profile-docpool:to_1_3_29')
    logger.info('Updated registry with new js/css paths')