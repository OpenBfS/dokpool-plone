## Python Script "isSituationDisplay"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

if getattr(context, "myELANCurrentSituation", None) is not None:
    return 1  # FIXME:
else:
    return False
