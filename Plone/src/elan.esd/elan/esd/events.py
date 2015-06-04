from zope.component import adapter
from docpool.base.interfaces import IDocumentPool
from docpool.base.events import IDocumentPoolInitializedEvent,\
    IDocumentPoolRemovedEvent
from elan.esd.utils import isElanEsdInstalled
from elan.esd.structures import esdAdded as esdAddedExtern

@adapter(IDocumentPool, IDocumentPoolInitializedEvent)
def esdAdded(obj, event=None):
    """
    """
    self = obj
    if isElanEsdInstalled(self):
        esdAddedExtern(self, event)
 
@adapter(IDocumentPool, IDocumentPoolRemovedEvent)
def esdRemoved(obj, event=None):
    """
    """
    self = obj
    if isElanEsdInstalled(self):
        pass
