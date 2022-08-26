from docpool.base.caching.etags import cacheTimes
from docpool.base.caching.interfaces import IAppCaching
from docpool.event.utils import getOpenScenarios
from plone import api
from zope.component import adapter
from zope.interface import Interface, implementer


@implementer(IAppCaching)
@adapter(Interface, Interface)
class AppCaching:
    def __init__(self, context, request):
        self.context = context
        self.request = request

    def etag_pieces(self):
        pieces = []

        if hasattr(self.context, "getUserSelectedScenarios"):
            scenarios = self.context.getUserSelectedScenarios()
            pieces.append(";".join(scenarios))

        user = api.user.get_current()
        filtered = user.getProperty("filter_active") or False
        pieces.append(str(filtered))

        scs = getOpenScenarios(self.context)
        all_scenarios = ";".join(s.id for s in scs if s.review_state == "published")
        pieces.append(all_scenarios)

        return pieces


cacheTimes.update(
    {
        "ELANArchive": 7200,
        "ELANCurrentSituation": 300,
        "ELANDocCollection": 300,
    }
)
