## Script (Python) "docpoolversion.py"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##
from Products.CMFCore.utils import getToolByName
from docpool.base.utils import execute_under_special_role
from Products.CMFQuickInstallerTool.QuickInstallerTool import QuickInstallerTool
qi = getToolByName(context, 'portal_quickinstaller')
v = execute_under_special_role(context, "Manager", QuickInstallerTool.getProductVersion, qi, 'docpool.base')
if v:
    return v
else:
    return "1.0"
