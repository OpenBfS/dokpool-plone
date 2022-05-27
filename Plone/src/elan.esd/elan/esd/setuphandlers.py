# -*- coding: utf-8 -*-
from plone import api
from zope.globalrequest import getRequest


def post_install(setup):
    catalog = api.portal.get_tool("portal_catalog")
    catalog.reindexIndex(["scenarios", "category"], REQUEST=getRequest())
