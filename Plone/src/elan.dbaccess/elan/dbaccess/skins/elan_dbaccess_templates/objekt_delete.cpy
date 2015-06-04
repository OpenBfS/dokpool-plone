## Controller Python Script "objekt_delete"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Loeschen von Objekten
##
from elan.dbaccess.utils import portalMessage, getTool

request = context.REQUEST
typ = request.get('typ')
single = request.get('single', False)

vpud = getTool()
vpud.objekteLoeschen(request, context)

log = u"Die Daten wurden gelöscht."  
portalMessage(context, log)

vpud.cleanForm(typ, request.form)

if single: # Wir kommen aus der Einzelanzeige, dann wollen wir keine Formularfelder im Request mehr haben
    state.setNextAction('redirect_to:string:objekt_liste?typ=%s' % typ)
else:
	state.setNextAction('traverse_to:string:objekt_liste?typ=%s' % typ)

return state
