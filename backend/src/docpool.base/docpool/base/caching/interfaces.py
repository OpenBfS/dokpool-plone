from zope.interface import Interface


class IAppCaching(Interface):
    def etag_pieces():
        """App-specific contribution to ETagValue"""
