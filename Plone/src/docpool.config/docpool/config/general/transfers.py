# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from plone import api

def install(self):
    """
    """
    fresh = True
    configUsers(self, fresh)

def configUsers(self, fresh):
    """
    """
    if fresh:
        mtool = getToolByName(self, "portal_membership")
        api.user.grant_roles(username='dpmanager', roles=['TransfersUser'])
        api.user.grant_roles(username='dpadmin', roles=['TransfersUser'])
