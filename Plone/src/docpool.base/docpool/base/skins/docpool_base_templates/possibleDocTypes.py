## Python Script "possibleDocTypes"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

from docpool.base.vocabularies import DocTypeVocabulary

aedt = DocTypeVocabulary()
#return [ a[0] for a in aedt(context, raw=True)]
return [ "%s|%s" % (a[0],a[1]) for a in aedt(context, raw=True, filtered=True)]


# 
# from Products.CMFPlone.utils import getToolByName
# 
# cat = getToolByName(context, "portal_catalog")
# aedt = cat(portal_type = 'DocType', sort_on="sortable_title")
# return [ t.id for t in aedt ]