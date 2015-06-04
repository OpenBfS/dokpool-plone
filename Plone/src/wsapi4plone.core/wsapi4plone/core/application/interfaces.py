# -*- coding: utf-8 -*-
from zope.interface import Interface
from wsapi4plone.core.interfaces import ICallbackExtension, IReadExtension


class IPloneContents(IReadExtension, ICallbackExtension):
    """An extension to get at Plone Folder items."""


class IContentsQuery(Interface):
    """Adapter to provide the query results for a given object."""

    def arguments(self):
        """Returns the arguments (in dictionary format) that are used to
        make the query for the contents."""

    def results(self):
        """A method to obtain the results from ZCatalog search."""
