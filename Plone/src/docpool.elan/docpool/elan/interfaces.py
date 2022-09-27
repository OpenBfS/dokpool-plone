from docpool.elan.content.dpevent import IDPEvent
from docpool.elan.content.dpevents import IDPEvents
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IDocpoolElanLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
