# -*- coding: utf-8 -*-
from zope.interface import Interface, Attribute
##code-section imports
from docpool.dbaccess import DocpoolMessageFactory as _
##/code-section imports

##code-section manual code
class Idbadmin(Interface):
    """
    Marker interface for .dbadmin
    """


class IProtectedEntityClass(Interface):
    """
    Marker-Interface fuer alle Entity-KLASSEN, welche ueber
    datenbezogene Berechtigungen geschuetzt werden.
    """

class IAuditing(Interface):
    """
    Implemented by all entities which support automatic logging of changes.
    All methods need a Plone context object 
    """
    def wasCreated(context):
        """
        """
        
    def wasUpdated(context):
        """
        """
        
    def wasDeleted(context):
        """
        """

class IDataSecurity(Interface):
    """
    Definiert Methoden zur Berechtigungspruefung
    """
    def can_access():
        """
        """
        
    def can_create():
        """
        """
        
    def can_read(item):
        """
        """
        
    def can_read_all():
        """
        """
        
    def can_update(item):
        """
        """
        
    def can_update_all():
        """
        """
        
    def can_delete(item):
        """
        """
        
    def can_delete_all():
        """
        """
        
    def setContextObj(context):
        """
        """
        
    def getContextObj():
        """
        """
        
    def currentUser():
        """
        """
        
    def setView(view):
        """
        """
        
    def getView():
        """
        """
##/code-section manual code