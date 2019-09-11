## Script (Python) "isReceiver.py"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Checks if a user has rights on transfer folders
##
try:
    from plone import api

    roles = api.user.get_roles(obj=context)
    if "Manager" in roles or "Site Administrator" in roles:
        return True
    groups = api.user.get_current().getGroups()
    for g in groups:
        if g.find("Receivers") > -1:
            return True
    return False
except:
    return False
