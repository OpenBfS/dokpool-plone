## Script (Python) "isAdmin.py"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Checks if a user has content administration rights
##
try:
    from plone import api

    roles = api.user.get_roles(obj=context)
    if roles and "Manager" in roles or "Site Administrator" in roles:
        return True
    return False
except Exception as e:
    return False
