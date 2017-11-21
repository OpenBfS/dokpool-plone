from AccessControl import Unauthorized
from zope.interface import Interface
from Products.CMFPlone.utils import log, log_exc
from zope.component.interfaces import ObjectEvent
from zope.interface import implements

class IDocumentPoolUndeleteable(Interface):
    """Marker interface for objects which should not be deleted.
    """

def delete_handler(object, event):
    """
    Called when an undeleteable object is removed. Only allowed for Managers.
    """
    log("Deleting protected object " + object.getId())
    try:
        if not object.isAdmin():
            raise Unauthorized
    except Exception, e:
        log_exc(e)

class IDocumentPoolInitializedEvent(Interface):
    """
    """
    
class DocumentPoolInitializedEvent(ObjectEvent):
    implements(IDocumentPoolInitializedEvent)

class IDocumentPoolRemovedEvent(Interface):
    """
    """
    
class DocumentPoolRemovedEvent(ObjectEvent):
    implements(IDocumentPoolRemovedEvent)