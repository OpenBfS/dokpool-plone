## Python Script "refresh_time"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from elan.esd.browser.viewlets.common import TimeViewlet
tv = TimeViewlet(context, context.REQUEST, None)
return tv.render()