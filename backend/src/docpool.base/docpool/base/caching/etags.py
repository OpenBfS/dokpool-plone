from plone.app.caching.interfaces import IETagValue
from plone.app.caching.operations.utils import getContext
from time import time
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.interface import Interface


@implementer(IETagValue)
@adapter(Interface, Interface)
class DokPoolApps:
    def __init__(self, published, request):
        self.published = published
        self.request = request

    def __call__(self):
        context = getContext(self.published)
        dp_app_state = getMultiAdapter((context, self.request), name="dp_app_state")
        apps = dp_app_state.effectiveAppsHere()
        pieces = [";".join(apps)]

        for app in apps:
            app_caching = queryMultiAdapter(
                (context, self.request), name=f"app_caching_{app}"
            )
            if app_caching:
                pieces.extend(app_caching.etag_pieces())

        return "-".join(pieces)


cacheTimes = {
    "DPDocument": 300,
    "GroupFolder": 300,
    "PrivateFolder": 300,
    "ReviewFolder": 300,
    "SimpleFolder": 300,
    "InfoDocument": 7200,
    "InfoFolder": 3600,
    "UserFolder": 300,
    "DPTransferFolder": 300,
    "Dashboard": 120,
}


@implementer(IETagValue)
@adapter(Interface, Interface)
class DokPoolCacheTime:
    """
    Hiervon Varianten je nach Typ:
    DPDocument -->
    Collection -->
    Gruppenordner / Private Ordner -->
    INFOOrdner -->
    """

    def __init__(self, published, request):
        self.published = published
        self.request = request

    def __call__(self):
        context = getContext(self.published)
        portalTypeName = context.getPortalTypeName()
        return str(time() // cacheTimes.get(portalTypeName, 3600))
