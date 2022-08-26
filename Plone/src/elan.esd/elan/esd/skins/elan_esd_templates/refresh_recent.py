## Python Script "refresh_time"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from elan.esd.portlets.recent import Renderer


rp = Renderer(context, context.REQUEST, None, None, None)
context.REQUEST.RESPONSE.setHeader("Cache-Control", "no-cache")

return rp.render()
