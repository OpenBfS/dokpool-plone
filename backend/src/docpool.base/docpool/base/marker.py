from zope.interface import Interface


class IImportingMarker(Interface):
    """
    A marker on the request used during importing with exportimport.
    """


class IAppActiveMarker(Interface):
    """
    Allow querying for app-active marker interfaces by app name.
    """
