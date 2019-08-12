# -*- coding: utf-8 -*-
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.users.browser.userdatapanel import UserDataConfiglet as UDC


class UserDataConfiglet(UDC):
    """Control panel version of the userdata panel"""

    template = ViewPageTemplateFile('account-configlet.pt')
