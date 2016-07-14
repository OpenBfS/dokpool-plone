## Controller Python Script "struct_save"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=
##title=Save a structured object
##
from docpool.dbaccess.utils import portalMessage, getTool
from Products.CMFPlone.utils import log, log_exc, safe_unicode
from docpool.dbaccess import ObjectDuplicateException
from docpool.dbaccess import DocpoolMessageFactory as _


request = context.REQUEST
typ = request.get('typ')
edit_url = request.get('edit_url')

vpud = getTool()
message = _(u"The data was saved.")
level = 'info'
action = 'redirect_to:string:%s' % edit_url

try:
    result = vpud.objektSpeichern(request, context)
    if result:
    	try:
    		pk = int(result)
    		action = action.replace('###', str(result))
    	except:
	        message = _(u"Please correct the following errors.")
	        level = 'error'
	        request.set('formerror', result)
	        action = 'traverse_to:string:struct_edit'
except ObjectDuplicateException, e:
    dublettenlinks = []
    for double in e.dubletten:
        dublettenlinks.append(vpud.prepareEditURL(typ, double))
    if dublettenlinks:
        request.set('dubletten', dublettenlinks)
    request.set('formerror', e.formular)
    action = 'traverse_to:string:struct_edit'
    message = _(u"There is a duplicate for this object!")
    level = 'error'
    
portalMessage(context, message, level)
state.setNextAction(action)

return state
