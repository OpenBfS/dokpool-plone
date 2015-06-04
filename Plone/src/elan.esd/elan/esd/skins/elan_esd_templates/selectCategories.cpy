## Python Script "selectCategories"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=cats=[]
##title=
##

from elan.esd.utils import setCategoriesForCurrentUser

setCategoriesForCurrentUser(context, cats)
context.redirectToReferrerWithParameters("Set category filter")