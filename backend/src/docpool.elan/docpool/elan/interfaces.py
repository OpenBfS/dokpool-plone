from docpool.elan.content.dpevent import IDPEvent  # noqa: F401
from docpool.elan.content.dpevents import IDPEvents  # noqa: F401
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IDocpoolElanLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
