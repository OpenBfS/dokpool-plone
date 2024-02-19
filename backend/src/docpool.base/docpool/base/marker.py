from zope.interface import Interface


class IImportingMarker(Interface):
    """
    A marker on the request used during importing with exportimport.
    """
