from docpool.base.content.infofolder import IInfoFolder
from docpool.base.content.infofolder import InfoFolder
from docpool.base.marker import IImportingMarker
from docpool.elan.config import ELAN_APP
from plone.supermodel import model
from zope.component import adapter
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.lifecycleevent import IObjectAddedEvent


class IELANInfos(model.Schema, IInfoFolder):
    """ """


@implementer(IELANInfos)
class ELANInfos(InfoFolder):
    """ """

    APP = ELAN_APP


@adapter(IELANInfos, IObjectAddedEvent)
def infosAdded(obj, event=None):
    """
    Set local role for Content Administrators
    """
    if IImportingMarker.providedBy(getRequest()):
        return

    self = obj
    esd = self.myDocumentPool()
    prefix = esd.prefix or esd.getId()
    prefix = str(prefix)
    self.manage_setLocalRoles("%s_ContentAdministrators" % prefix, ["ContentAdmin"])
