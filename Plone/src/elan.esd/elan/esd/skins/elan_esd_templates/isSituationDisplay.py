## Python Script "isSituationDisplay"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from docpool.elan.config import ELAN_APP


if getattr(context, "myDocumentPool", None) is not None:
    return context.isActive(ELAN_APP)
else:
    return False
