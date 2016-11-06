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

class ChannelSecurity(DefaultSecurity):
    """
    """
    implements(IDataSecurity)
    #adapts(ISubscriptionSupport)
    adapts(IELANProtectedEntityClass, IBasicUser)
    
    def __init__(self, klass, user):
        DefaultSecurity.__init__(self, klass, user)
        self.isManager = user.has_role("Manager")
        
    def can_access(self):
        from elan.esd.content.elantransferfolder import IELANTransferFolder
        context = self.getContextObj()
        if not IELANTransferFolder.providedBy(context):
            #print "NOT"
            if self.isManager:
                return True
            else:
                return False
        return self.can_delete_all() or checkLocalRole(context, "Site Administrator")
            
    def can_delete(self, item):
        """
        """
        return self.can_delete_all()
    
    def can_delete_all(self):
        """
        """
        # print "can_delete_all"
        # print self.user
        # print self.context
        return self.isManager or self.user.has_role("Owner", self.getContextObj())
    
    def can_update(self, item):
        """
        """
        return self.can_delete_all()
