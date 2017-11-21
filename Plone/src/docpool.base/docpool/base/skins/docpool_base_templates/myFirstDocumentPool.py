## Python Script "myESDs"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from AccessControl import Unauthorized
esd = context.myPersonalDocumentPool()
if esd:
    return esd.absolute_url()
else:
    raise Unauthorized()

