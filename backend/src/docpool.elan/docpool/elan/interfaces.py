from docpool.elan.config import ELAN_APP
from docpool.elan.content.dpevent import IDPEvent  # noqa: F401
from docpool.elan.content.dpevents import IDPEvents  # noqa: F401
from zope.interface import Interface
from zope.interface import named
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IDocpoolElanLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


@named(ELAN_APP)
class IELANActive(Interface):
    """Marker interface to signal ELAN is active in a context.

    Meant to be applied as a layer to the request during traversal.
    """
