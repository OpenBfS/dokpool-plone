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
    pass
