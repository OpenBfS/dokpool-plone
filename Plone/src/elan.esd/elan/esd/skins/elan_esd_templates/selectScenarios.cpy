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

from docpool.event.utils import setScenariosForCurrentUser

#scnrs = REQUEST.get("scnrs", [])

setScenariosForCurrentUser(context, scnrs)
context.REQUEST.response.setHeader("Pragma", "no-cache")
context.redirectToReferrerWithParameters("Set filter")