# -*- coding: utf-8 -*- 
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
    from docpool.base.utils import getGroupsForCurrentUser
    roles = api.user.get_roles(obj=context)
    if roles and "Reader" in roles:
        gs = getGroupsForCurrentUser(context)
        if len(gs) > 1:
            return True
        else:
            return False
    return True
except Exception, e:
    return False