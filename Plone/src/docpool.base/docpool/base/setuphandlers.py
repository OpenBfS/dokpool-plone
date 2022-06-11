from plone import api
from Products.CMFCore.utils import getToolByName
from zope.globalrequest import getRequest


def post_install(context):
    portal = api.portal.get()
    from docpool.config.general.base import install
    install(portal)
    cat = getToolByName(portal, "portal_catalog")
    cat.reindexIndex(["dp_type", "mdate", "changed"], REQUEST=getRequest())
