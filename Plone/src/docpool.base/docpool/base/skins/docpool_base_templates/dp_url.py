## Python Script "dp_url"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from Products.Archetypes.utils import shasattr

if shasattr(context, "myDocumentPool", True):
    return context.myDocumentPool().absolute_url()
else:
    return context.portal_url()
