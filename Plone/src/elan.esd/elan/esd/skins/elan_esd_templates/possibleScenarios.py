## Python Script "possibleScenarios"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

from elan.esd.utils import getActiveScenarios

aedt = getActiveScenarios(context)
return [ (t.getId, t.Title) for t in aedt ]