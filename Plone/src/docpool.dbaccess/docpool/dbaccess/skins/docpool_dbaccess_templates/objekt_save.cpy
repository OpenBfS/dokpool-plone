## Controller Python Script "objekt_save"
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
from Products.CMFPlone.utils import log, log_exc, safe_unicode
from docpool.dbaccess import ObjectDuplicateException

request = context.REQUEST
typ = request.get('typ')

vpud = getTool()
message = u"Ihre Daten wurden gespeichert."
level = 'info'
action = 'redirect_to:string:%s/objekt_liste?typ=%s' % (context.absolute_url(), typ)

try:
    result = vpud.objektSpeichern(request, context)
    if result:
        message = "Bitte korrigieren Sie die Angaben."
        level = 'error'
        request.set('formerror', result)
        action = 'traverse_to:string:objekt_edit'
except ObjectDuplicateException, e:
    dublettenlinks = []
    for double in e.dubletten:
        dublettenlinks.append(vpud.prepareEditURL(typ, double))
    if dublettenlinks:
        request.set('dubletten', dublettenlinks)
    request.set('formerror', e.formular)
    action = 'traverse_to:string:objekt_edit'
    message = u"Dieser Datensatz ist bereits vorhanden!"
    level = 'error'
    
portalMessage(context, message, level)
state.setNextAction(action)

return state
