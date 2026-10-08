from docpool.rei.config import REI_APP
from zope.interface import Interface
from zope.interface import named


class IReiMarker(Interface):
    """Marker interface that defines a Zope 3 browser layer."""


@named(REI_APP)
class IREIActive(Interface):
    """Request marker for the active REI application."""
