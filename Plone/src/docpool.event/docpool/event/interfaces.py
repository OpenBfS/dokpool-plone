from docpool.event.content.dpevent import IDPEvent  # noqa: F401
from docpool.event.content.dpevents import IDPEvents  # noqa: F401
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IDocpoolEventLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
