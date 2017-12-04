from plone.app.caching.operations.etags import LastModified
from plone.app.caching.operations.utils import getContext
from plone.app.caching.interfaces import IETagValue

from zope.interface import implements
from zope.interface import Interface
from zope.interface import implementer

from zope.component import adapts, getMultiAdapter
from zope.component import adapter

from time import time

@implementer(IETagValue)
@adapter(Interface, Interface)
class DokPoolApps(object):
    """
    """

    def __init__(self, published, request):
        self.published = published
        self.request = request

    def __call__(self):
        context = getContext(self.published)
        dp_app_state = getMultiAdapter((context, self.request), name=u'dp_app_state')
        apps = ";".join(dp_app_state.effectiveAppsHere())
        return apps

cacheTimes = {
    "DPDocument" : 300,
    "GroupFolder" : 300,
    "PrivateFolder" : 300,
    "ReviewFolder" : 300,
    "SimpleFolder" : 300,
    "InfoDocument" : 7200,
    "InfoFolder" : 3600,
    "UserFolder" : 300,
    "ELANArchive" : 7200,
    "ELANCurrentSituation" : 3600,
    "ELANDocCollection" : 300,
    "ELANTransferFolder" : 300,
}

@implementer(IETagValue)
@adapter(Interface, Interface)
class DokPoolCacheTime(object):
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

