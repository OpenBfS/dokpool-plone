## Python Script "isArchive"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

return "archive" in context.getPhysicalPath()
