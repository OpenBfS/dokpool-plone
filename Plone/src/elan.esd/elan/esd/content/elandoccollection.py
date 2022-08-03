from docpool.base.content.dashboardcollection import DashboardCollection
from docpool.base.content.dashboardcollection import IDashboardCollection
from docpool.base.marker import IImportingMarker
from elan.esd import DocpoolMessageFactory as _
from plone.supermodel import model
from Products.CMFCore.utils import getToolByName
from zope.component import adapter
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.lifecycleevent.interfaces import IObjectAddedEvent, IObjectModifiedEvent


class IELANDocCollection(model.Schema, IDashboardCollection):
    """Same as IDashboardCollection"""


@implementer(IELANDocCollection)
class ELANDocCollection(DashboardCollection):
    """DashboardCollection with a different portal_type"""


@adapter(IELANDocCollection, IObjectModifiedEvent)
def update_docTypes(obj, event=None):
    if IImportingMarker.providedBy(getRequest()):
        return
    if obj:
        # print "update_docTypes", obj.docTypes
        obj.setDocTypesUpdateCollection()
        obj.reindexObject()


@adapter(IELANDocCollection, IObjectAddedEvent)
def enableSyndication(obj, event=None):
    if IImportingMarker.providedBy(getRequest()):
        return

    syn_tool = getToolByName(obj, "portal_syndication", None)
    if syn_tool is not None:
        if syn_tool.isSiteSyndicationAllowed() and not syn_tool.isSyndicationAllowed(
            obj
        ):
            syn_tool.enableSyndication(obj)
