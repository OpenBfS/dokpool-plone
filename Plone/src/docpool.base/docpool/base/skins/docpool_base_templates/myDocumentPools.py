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

cat = getToolByName(context, 'portal_catalog', None)
esds = cat(portal_type="DocumentPool", sort_on="sortable_title")
esds = [(brain.getURL(), brain.Title) for brain in esds]
return esds
