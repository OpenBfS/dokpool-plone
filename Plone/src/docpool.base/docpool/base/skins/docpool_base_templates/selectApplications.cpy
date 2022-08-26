## Python Script "selectApplications"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=apps=[]
##title=
##

from docpool.base.utils import setApplicationsForCurrentUser

setApplicationsForCurrentUser(context, apps)
context.redirectToReferrerWithParameters("Set application filter")
