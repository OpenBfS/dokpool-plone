# -*- coding: utf-8 -*-

__author__ = 'Condat AG'
__docformat__ = 'plaintext'

from datetime import datetime
from docpool.dbaccess.dbinit import __metadata__
from docpool.dbaccess.dbinit import __session__
from docpool.dbaccess.interfaces import IAuditing
from elixir import *
from Products.CMFPlone.utils import getToolByName
from zope.interface import implementer


metadata = __metadata__
session = __session__


@implementer(IAuditing)
class Item(Entity):
    """
    Oberklasse fuer Aenderungsverfolgung
    """
    using_options(
        tablename='vpauditlogs',
        inheritance='multi',
        polymorphic=False)

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
