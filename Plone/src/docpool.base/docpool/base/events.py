from AccessControl import Unauthorized
from OFS.interfaces import IObjectWillBeRemovedEvent
from plone.base.interfaces.siteroot import IPloneSiteRoot
from Products.CMFPlone.utils import log
from Products.CMFPlone.utils import log_exc
from zope.component import adapter
from zope.interface.interfaces import ObjectEvent
from zope.interface import implementer
from zope.interface import Interface


class IDocumentPoolUndeleteable(Interface):
    """Marker interface for objects which should not be deleted.
    """


@adapter(IDocumentPoolUndeleteable, IObjectWillBeRemovedEvent)
def delete_handler(object, event):
    """
    Called when an undeleteable object is removed. Only allowed for Managers.
    """
    if IPloneSiteRoot.providedBy(event.object):
        return

    log("Deleting protected object " + object.getId())
    try:
        if not object.isAdmin():
            raise Unauthorized
    except Exception as e:
        log_exc(e)


class IDocumentPoolInitializedEvent(Interface):
    """
    """


@implementer(IDocumentPoolInitializedEvent)
class DocumentPoolInitializedEvent(ObjectEvent):
    pass


class IDocumentPoolRemovedEvent(Interface):
    """
    """


@implementer(IDocumentPoolRemovedEvent)
class DocumentPoolRemovedEvent(ObjectEvent):
    pass