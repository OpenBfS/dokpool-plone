# -*- coding: utf-8 -*-
from zope.interface import implements
from zope.component import adapts

from elan.dbaccess.interfaces import IDataSecurity
from elan.dbaccess.security import DefaultSecurity
from Products.PluggableAuthService.interfaces.authservice import IBasicUser
from docpool.base.utils import checkLocalRole

from elan.dbaccess.interfaces import IProtectedEntityClass

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
        return checkLocalRole(context, "Site Administrator")
            
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
