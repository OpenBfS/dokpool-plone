from AccessControl import Unauthorized
from docpool.base.utils import is_admin
from OFS.interfaces import IObjectWillBeRemovedEvent
from plone.base.interfaces.siteroot import IPloneSiteRoot
from Products.CMFPlone.utils import log
from Products.CMFPlone.utils import log_exc
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface
from zope.interface.interfaces import ObjectEvent


class IDocumentPoolUndeleteable(Interface):
    """Marker interface for objects which should not be deleted."""


@adapter(IDocumentPoolUndeleteable, IObjectWillBeRemovedEvent)
def delete_handler(object, event):
    """
    Called when an undeleteable object is removed. Only allowed for Managers.
    """
    if IPloneSiteRoot.providedBy(event.object):
        return

    log("Deleting protected object " + object.getId())
    try:
        if not is_admin(object):
            raise Unauthorized
    except Exception as e:
        log_exc(e)


class IDocumentPoolInitializedEvent(Interface):
    """ """


@implementer(IDocumentPoolInitializedEvent)
class DocumentPoolInitializedEvent(ObjectEvent):
    pass


class IDocumentPoolRemovedEvent(Interface):
    """ """


@implementer(IDocumentPoolRemovedEvent)
class DocumentPoolRemovedEvent(ObjectEvent):
    pass
