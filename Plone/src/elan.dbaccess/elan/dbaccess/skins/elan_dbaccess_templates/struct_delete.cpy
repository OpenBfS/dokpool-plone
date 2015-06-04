## Controller Python Script "struct_delete"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Delete objects
##
from elan.dbaccess.utils import portalMessage, getTool
from elan.dbaccess import ELAN_EMessageFactory as _

request = context.REQUEST
typ = request.get('typ')
single = request.get('single', False)
edit_url = request.get('herkunft')
action = 'redirect_to:string:%s' % edit_url

vpud = getTool()
vpud.objekteLoeschen(request, context)

log = _(u"Data was deleted.")  
portalMessage(context, log)

vpud.cleanForm(typ, request.form)

state.setNextAction(action)

return state
