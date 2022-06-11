from plone import api
from plone.app.caching.interfaces import IETagValue
from plone.app.caching.operations.utils import getContext
from time import time
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.interface import implementer
from zope.interface import Interface
from docpool.event.utils import getOpenScenarios

@implementer(IETagValue)
@adapter(Interface, Interface)
class DokPoolApps:
    """
    """

    def __init__(self, published, request):
        self.published = published
        self.request = request

    def __call__(self):
        context = getContext(self.published)
        dp_app_state = getMultiAdapter(
            (context, self.request), name='dp_app_state')
        apps = ";".join(dp_app_state.effectiveAppsHere())

        scenarios = ""
        if hasattr(context, "getUserSelectedScenarios"):
            scenarios = context.getUserSelectedScenarios()
            scenarios = ";".join(scenarios)

        scs = getOpenScenarios(context)
        all_scenarios = ";".join(
            s.id for s in scs if s.review_state == "published")

        user = api.user.get_current()
        filtered = user.getProperty("filter_active") or False

        return "-".join([apps, scenarios, str(filtered), all_scenarios])


cacheTimes = {
    "DPDocument": 300,
    "GroupFolder": 300,
    "PrivateFolder": 300,
    "ReviewFolder": 300,
    "SimpleFolder": 300,
    "InfoDocument": 7200,
    "InfoFolder": 3600,
    "UserFolder": 300,
    "ELANArchive": 7200,
    "ELANCurrentSituation": 300,
    "ELANDocCollection": 300,
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
