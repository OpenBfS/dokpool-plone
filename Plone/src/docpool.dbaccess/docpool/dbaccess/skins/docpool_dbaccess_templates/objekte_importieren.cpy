## Controller Python Script "importieren"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=typ, importfile
##title=Importieren von CSV-Daten
##
from docpool.dbaccess.utils import portalMessage, getTool


request = context.REQUEST

vpud = getTool()
meldung, status = vpud.objekteImportieren(typ, importfile, request, context)

if len(meldung) == 1: # Es hat richtig gekracht
    log = "Fehler beim Import: %s" % meldung[0]    
    action = 'redirect_to:string:objekt_liste?typ=%s' % typ
    portalMessage(context, log, type='error')
else:
    if status:
        log = u"Die Daten wurden ohne Fehler importiert."
        portalMessage(context, log)
    else:
        log = u"Es gab Fehler beim Import."
        portalMessage(context, log, type='error')    
    action = 'traverse_to:string:import_meldung?typ=%s' % typ
    request.set("meldung", "\n".join(meldung))
state.setNextAction(action)

return state
