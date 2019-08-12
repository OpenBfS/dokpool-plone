## Python Script "possibleScenarios"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

from docpool.base.vocabularies import DocumentPoolVocabulary

aedt = DocumentPoolVocabulary()
# return [ a[0] for a in aedt(context, raw=True)]
return ["%s|%s" % (a[0], a[1]) for a in aedt(context, raw=True)]
