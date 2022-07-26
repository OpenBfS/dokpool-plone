#
# File: elaninfos.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ""
__docformat__ = "plaintext"

"""Definition of the ELANInfos content type. See elaninfos.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from docpool.base.content.infofolder import IInfoFolder, InfoFolder
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

    security = ClassSecurityInfo()

    APP = ELAN_APP

    def myELANInfos(self):
        """ """
        return self

    def getFirstChild(self):
        """ """
        fc = self.getFolderContents()
        if len(fc) > 0:
            return fc[0].getObject()
        else:
            return None

    def getAllContentObjects(self):
        """ """
        return [obj.getObject() for obj in self.getFolderContents()]

    def getInfoDocuments(self, **kwargs):
        """ """
        args = {"portal_type": "InfoDocument"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getInfoFolders(self, **kwargs):
        """ """
        args = {"portal_type": "InfoFolder"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getInfoFolders(self, **kwargs):
        """ """
        args = {"portal_type": "InfoFolder"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getInfoLinks(self, **kwargs):
        """ """
        args = {"portal_type": "InfoLink"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]


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
