## Python Script "setActiveApp"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=activateFilter=False
##title=
##

from docpool.base.utils import activateAppFilter

activateAppFilter(context, activateFilter)
return context.REQUEST.RESPONSE.redirect(context.absolute_url())
