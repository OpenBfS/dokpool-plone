from plone.app.users.browser.userdatapanel import UserDataConfiglet as UDC
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class UserDataConfiglet(UDC):
    """Control panel version of the userdata panel"""

    template = ViewPageTemplateFile('account-configlet.pt')
