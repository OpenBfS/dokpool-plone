## Script (Python) "migrateELANTransfers.py"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Checks if a user has rights on transfer folders
##
from Products.CMFCore.utils import getToolByName

cat = getToolByName(context, 'portal_catalog', None)

transfers = cat(portal_type="ELANScenarios", sort_on = "sortable_title")
for transfer in transfers:
    t = transfer.getObject()
    print t
    t.migrate()

transfers = cat(portal_type="ELANScenario", sort_on = "sortable_title")
for transfer in transfers:
    t = transfer.getObject()
    print t
    t.migrate()

return "done"



