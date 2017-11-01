# -*- coding: utf-8 -*- 
## Python Script "possibleScenarios"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from docpool.base.utils import possibleDocumentPools

dps = possibleDocumentPools(context)
res = [ "" ]
res.extend([ "%s|%s" % (dp.UID, dp.Title) for dp in dps])
return res