## Python Script "myESDs"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.utils import shasattr
from AccessControl import Unauthorized
from plone import api
from Products.CMFPlone.utils import log

user = api.user.get_current()
username = user.getUserName()
parts = username.split("_")
esd_prefix = parts[0]


cat = getToolByName(context, 'portal_catalog', None)
esds = cat(portal_type="DocumentPool", sort_on = "sortable_title")
log(esds)
if esds:
    for esd in esds:
        obj = esd.getObject()
        if obj.myPrefix() == esd_prefix:
            return obj
    return esds[0].getObject()