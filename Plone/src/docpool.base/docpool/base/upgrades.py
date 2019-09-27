# -*- coding: utf-8 -*-
import logging


logger = logging.getLogger(__name__)

def to_1_3_29(context):
    context.runAllImportStepsFromProfile('profile-docpool.base:to_1_3_29')
    logger.info('Updated registry with new js/css paths')