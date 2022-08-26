from docpool.event import DocpoolMessageFactory as _
from docpool.event.content.dpevent import IDPEvent
from docpool.event.content.dpevents import IDPEvents
from zope.interface import Attribute
from zope.interface import Interface
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


class IDocpoolEventLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""
