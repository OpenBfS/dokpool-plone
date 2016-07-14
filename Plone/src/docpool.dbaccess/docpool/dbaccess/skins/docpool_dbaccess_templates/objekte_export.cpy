## Controller Python Script "objekte_export"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Exportieren von Objekten
##
from docpool.dbaccess.utils import portalMessage, getTool
from Products.CMFPlone.utils import log

request = context.REQUEST
dba = getTool()

typ = request.get('typ')
sort_on = request.form.get('sort_on') or dba.sort_default(typ) 
sort_order = request.form.get('sort_order') or 'ascending'
filter = dba.getRequestFilter(typ, request)
exportname = request.form.get('exportname', 'Standard')

#log(filter)
    
return dba.exportObjekte(typ=typ, sort_on=sort_on, sort_order=sort_order, filter=filter, exportname=exportname)
