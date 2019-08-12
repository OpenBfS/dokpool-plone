# -*- coding: utf-8 -*-
from zope.interface import implements
from zope.component import adapts

from docpool.dbaccess.interfaces import IDataSecurity
from docpool.dbaccess.security import DefaultSecurity
from Products.PluggableAuthService.interfaces.authservice import IBasicUser
from docpool.base.utils import checkLocalRole

from docpool.dbaccess.interfaces import IProtectedEntityClass


class IELANProtectedEntityClass(IProtectedEntityClass):
    pass


class IRIXSecurity(DefaultSecurity):
    """
    """

    implements(IDataSecurity)
    # adapts(ISubscriptionSupport)
    adapts(IELANProtectedEntityClass, IBasicUser)

    def __init__(self, klass, user):
        DefaultSecurity.__init__(self, klass, user)
        self.isManager = user.has_role("Manager") or user.has_role("Site Administrator")

    def can_access(self):
        return self.isManager

    def can_delete(self, item):
        """
        """
        return self.isManager

    def can_delete_all(self):
        """
        """
        return self.isManager

    def can_update(self, item):
        """
        """
        return self.can_access()
