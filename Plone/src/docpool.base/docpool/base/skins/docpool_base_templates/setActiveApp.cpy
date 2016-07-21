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

setApplicationsForCurrentUser(context, [ app ])
return context.REQUEST.RESPONSE.redirect(context.absolute_url())
