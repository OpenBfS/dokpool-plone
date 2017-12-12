## Python Script "activeScenarios"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

from elan.esd.utils import getActiveScenarios

return getActiveScenarios(context)
