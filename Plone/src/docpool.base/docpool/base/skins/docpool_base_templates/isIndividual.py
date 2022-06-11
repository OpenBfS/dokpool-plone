## Python Script "isPersonal"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

return "Members" in context.getPhysicalPath() and context.getId() != "Members"
