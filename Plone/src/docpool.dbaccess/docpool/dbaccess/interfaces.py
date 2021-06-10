# -*- coding: utf-8 -*-
from zope.interface import Interface, Attribute
from docpool.dbaccess import DocpoolMessageFactory as _


class Idbadmin(Interface):
    """
    Marker interface for .dbadmin
    """


class IProtectedEntityClass(Interface):
    """
    Marker-Interface fuer alle Entity-KLASSEN, welche ueber
    datenbezogene Berechtigungen geschuetzt werden.
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
