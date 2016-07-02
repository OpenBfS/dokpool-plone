# -*- coding: utf-8 -*-
import transaction
from Products.Archetypes.utils import shasattr
from Products.CMFCore.utils import getToolByName
from zExceptions import BadRequest
from plone.app.dexterity.behaviors.exclfromnav import IExcludeFromNavigation
from Products.CMFPlone.utils import log, log_exc
from elan.esd import DocpoolMessageFactory as _
from docpool.base.appregistry import activeApps, APP_REGISTRY



def docPoolAdded(obj, event=None):
    """
    """
    self = obj
    # Trigger configs for all applications
    for app in activeApps():
        APP_REGISTRY[app]['dpAddedMethod'](self)
# documentpool.esdAdded = esdAdded

def docPoolRemoved(obj, event=None):
    """
    """
    self = obj
    for app in activeApps():
        APP_REGISTRY[app]['dpRemovedMethod'](self)
    # Trigger configs for all applications


