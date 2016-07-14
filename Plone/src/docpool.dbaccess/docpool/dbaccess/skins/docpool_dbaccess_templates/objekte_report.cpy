## Controller Python Script "objekte_report"
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
reportname = request.get('reportname', 'Standard')

return dba.reportObjekte(reportcontext=context, typ=typ, sort_on=sort_on, sort_order=sort_order, filter=filter, reportname=reportname)
