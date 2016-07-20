# -*- coding: utf-8 -*-

__author__ = 'Condat AG'
__docformat__ = 'plaintext'

from docpool.dbaccess.dbinit import __metadata__, __session__

metadata = __metadata__
session = __session__

from elixir import *

from docpool.dbaccess.interfaces import IAuditing
from Products.CMFPlone.utils import getToolByName
from datetime import datetime
from zope.interface.declarations import implements


    
class Item(Entity):
    """
    Oberklasse fuer Aenderungsverfolgung
    """
    implements(IAuditing)
    using_options(tablename='vpauditlogs', inheritance='multi', polymorphic=False)

    erzeugungsnutzer = Field(Unicode(20))
    erzeugungsdatum = Field(DateTime(), default=datetime.now)
    aenderungsnutzer = Field(Unicode(20))
    aenderungsdatum = Field(DateTime())
    
    def _username(self, context):
        """
        """
        mtool = getToolByName(context, 'portal_membership')
        return mtool.getAuthenticatedMember().getUserName()
    
    def wasCreated(self, context):
        """
        """
        # print "executing wasCreated"
        self.erzeugungsdatum = datetime.now()
        self.aenderungsdatum = self.erzeugungsdatum
        self.erzeugungsnutzer = self._username(context)
        self.aenderungsnutzer = self.erzeugungsnutzer
        
        
    def wasUpdated(self, context):
        """
        """
        self.aenderungsdatum = datetime.now()
        self.aenderungsnutzer = self._username(context)
        
    def wasDeleted(self, context):
        """
        Nichts zu tun, weil kein Datensatz uebrig bleibt.
        """
        pass
    