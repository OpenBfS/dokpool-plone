## Python Script "setActiveApp"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=app=None
##title=
##

from docpool.base.utils import setApplicationsForCurrentUser
from docpool.base.utils import activateAppFilter


setApplicationsForCurrentUser(context, [ app ])
activateAppFilter(context, True)
absurl = context.absolute_url() 
if not 'content' in absurl:
  if app == 'base':
    absurl = context.myDocumentPool().absolute_url()
  if app == 'elan':
    absurl = context.myDocumentPool().absolute_url() + '/esd'
  if app == 'doksys':
    absurl = context.myDocumentPool().absolute_url() + '/searches'
  if app == 'rodos':
    absurl = context.myDocumentPool().absolute_url() + '/rodos'
return context.REQUEST.RESPONSE.redirect(absurl)
