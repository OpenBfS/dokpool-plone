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

from Products.CMFPlone.utils import safe_unicode
from elan.esd.utils import setCategoriesForCurrentUser

try:
   if len(cats[0]) != 1:
      try:
         cats_u = [safe_unicode(c) for c in cats]
      except:
         cats_u = cats
   else:
      cats_u = [safe_unicode(cats)]
except:
   cats_u = cats


setCategoriesForCurrentUser(context,cats_u)
context.redirectToReferrerWithParameters("Set category filter")
