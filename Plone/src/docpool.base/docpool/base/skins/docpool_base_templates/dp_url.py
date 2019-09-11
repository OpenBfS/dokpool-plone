## Python Script "dp_url"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

if getattr(context, "myDocumentPool", None) is not None:
    return context.myDocumentPool().absolute_url()
else:
    return context.portal_url()
