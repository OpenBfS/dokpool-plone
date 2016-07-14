## Controller Python Script "objekte_save"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Speichern eines Objekts
##
from docpool.dbaccess.utils import portalMessage, getTool
from docpool.dbaccess import DocpoolMessageFactory as _

request = context.REQUEST
typ = request.get('typ')

vpud = getTool()
vpud.objekteSpeichern(request, context)

log = _(u"Your data has been saved.")  
portalMessage(context, log)
state.setNextAction('redirect_to:string:objekt_liste?typ=%s' % typ)

return state
