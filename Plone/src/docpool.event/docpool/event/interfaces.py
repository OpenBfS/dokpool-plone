from zope.interface import Interface, Attribute
from docpool.event.content.dpevent import IDPEvent
from docpool.event.content.dpevents import IDPEvents
from docpool.event import DocpoolMessageFactory as _
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IDocpoolEventLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
