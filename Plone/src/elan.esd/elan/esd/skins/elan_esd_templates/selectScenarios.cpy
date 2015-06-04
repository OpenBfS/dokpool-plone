## Python Script "selectScenarios"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=scnrs=[]
##title=
##

from elan.esd.utils import setScenariosForCurrentUser

#scnrs = REQUEST.get("scnrs", [])

setScenariosForCurrentUser(context, scnrs)
context.redirectToReferrerWithParameters("Set scenario filter")