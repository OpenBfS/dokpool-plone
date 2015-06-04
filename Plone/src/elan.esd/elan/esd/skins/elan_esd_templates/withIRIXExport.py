## Python Script "withIRIXExport"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

try:
    if context.getPortalTypeName() == 'DPDocument':
        context.restrictedTraverse('contentconfig/irix')
        return True
except:
    pass
return False