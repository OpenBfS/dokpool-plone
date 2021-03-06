# -*- coding: utf-8 -*-
from docpool.dbaccess.interfaces import IDataSecurity
from docpool.dbaccess.interfaces import IProtectedEntityClass
from Products.PluggableAuthService.interfaces.authservice import IBasicUser
from zope.component import adapter
from zope.interface import implementer


@implementer(IDataSecurity)
@adapter(IProtectedEntityClass, IBasicUser)
class DefaultSecurity(object):
    """
    """
    # adapts(ISubscriptionSupport)

    def __init__(self, klass, user):
        # print "Default"
        self.klass = klass
        self.user = user
        self.isManager = user.has_role("Manager")

    def can_access(self):
        """
        """
        return self.isManager

    def can_create(self):
        """
        """
        return self.isManager

    def can_read(self, item):
        """
        """
        return self.isManager

    def can_read_all(self):
        """
        """
        return self.isManager

    def can_update(self, item):
        """
        """
        return self.isManager

    def can_update_all(self):
        """
        """
        return self.isManager

    def can_delete(self, item):
        """
        """
        return self.isManager

    def can_delete_all(self):
        """
        """
        return self.isManager

    def setContextObj(self, context):
        """
        """
        self.context = context

    def getContextObj(self):
        """
        """
        return self.context

    def currentUser(self):
        """
        """
        return self.user

    def setView(self, view):
        """
        """
        self.view = view

    def getView(self):
        """
        """
        return self.view
