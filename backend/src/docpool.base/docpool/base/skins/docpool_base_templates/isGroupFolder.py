## Python Script "isGroupFolder"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

return "Groups" in context.getPhysicalPath() and context.getId() != "Groups"
