## Python Script "isSituationDisplay"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from Products.Archetypes.utils import shasattr

if shasattr(context, "myELANCurrentSituation", acquire=True):
    return 1  # FIXME:
else:
    return False
