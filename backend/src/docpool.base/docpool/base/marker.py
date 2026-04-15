from zope.interface import Interface


class IImportingMarker(Interface):
    """
    A marker on the request used during importing with exportimport.
    """


class IAppActiveMarker(Interface):
    """
    Allow querying for app-active marker interfaces by app name.
    """


class IJournalContainerMarker(Interface):
    """
    Marker for containers containing journals.
    """


class IJournalEntryMarker(Interface):
    """
    Marker for journal entries applied after creation.
    """
