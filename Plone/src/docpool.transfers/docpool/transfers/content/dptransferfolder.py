#
# File: dptransferfolder.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ""
__docformat__ = "plaintext"

"""Definition of the DPTransferFolder content type. See dptransferfolder.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from docpool.base.content.archiving import IArchiving
from docpool.base.content.doctype import IDocType
from docpool.base.content.documentpool import IDocumentPool
from docpool.base.content.folderbase import FolderBase
from docpool.base.content.folderbase import IFolderBase
from docpool.base.marker import IImportingMarker
from docpool.base.utils import _copyPaste
from docpool.base.utils import execute_under_special_role
from docpool.base.utils import queryForObject
from docpool.base.utils import queryForObjects
from docpool.transfers import DocpoolMessageFactory as _
from logging import getLogger
from persistent.mapping import PersistentMapping
from plone import api
from plone.base.interfaces.siteroot import IPloneSiteRoot
from plone.dexterity.interfaces import IEditFinishedEvent
from plone.supermodel import model
from Products.CMFPlone.utils import log
from Products.CMFPlone.utils import parent
from zope import schema
from zope.component import adapter
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectRemovedEvent


logger = getLogger("dptransferfolder")


HAS_ELAN = True
try:
    from docpool.elan.config import ELAN_APP
except ImportError:
    HAS_ELAN = False


class IDPTransferFolder(model.Schema, IFolderBase):
    """ """

    sendingESD = schema.Choice(
        title=_(
            "label_dptransferfolder_sendingesd",
            default="The organisation sending content via this transfer folder",
        ),
        description=_("description_dptransferfolder_sendingesd", default=""),
        required=True,
        source="docpool.base.vocabularies.DocumentPools",
    )

    permLevel = schema.Choice(
        title=_("label_dptransferfolder_permlevel", default="Permission level"),
        description=_("description_dptransferfolder_permlevel", default=""),
        required=True,
        default="read/write",
        source="docpool.transfers.vocabularies.Permissions",
    )

    doctypePermissions = schema.Dict(
        title=_(
            "label_dptransferfolder_doctypepermissions",
            default="Permissions by document type",
        ),
        value_type=schema.Choice(
            required=True,
            source="docpool.transfers.vocabularies.DTPermOptions",
        ),
        key_type=schema.TextLine(),
    )

    unknownDtDefault = schema.Choice(
        title=_(
            "label_dptransferfolder_unknowndtdefault",
            default="Default for unknown document types",
        ),
        description=_("description_dptransferfolder_unknowndtdefault", default=""),
        required=True,
        default="block",
        source="docpool.transfers.vocabularies.UnknownOptions",
    )

    unknownScenDefault = schema.Choice(
        title=_(
            "label_dptransferfolder_unknownscendefault",
            default="Default for unknown scenarios",
        ),
        description=_("description_dptransferfolder_unknownscendefault", default=""),
        required=True,
        default="block",
        source="docpool.transfers.vocabularies.UnknownOptions",
    )


@implementer(IDPTransferFolder)
class DPTransferFolder(FolderBase):
    """ """

    security = ClassSecurityInfo()

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.doctypePermissions = PersistentMapping()

    # TODO should be indexed
    def from_to_title(self):
        from_title = self.getSendingESD().Title()
        to_title = self.myDocumentPool().Title()
        return f"{from_title} --> {to_title} ({self.title})"

    def acceptsDT(self, dt_id):
        """
        Do I specifically accept this doc type?
        """
        perm = self.doctypePermissions.get(dt_id, False)
        return perm and perm != "block"

    def getMatchingDocumentTypes(self, ids_only=True):
        """ """

        def doIt():
            esd = self.getSendingESD()
            theirDts = esd.myDocumentTypes(ids_only=True)
            myDts = self.myDocumentTypes()
            # print theirDts
            # print myDts
            if ids_only:
                return [dt[0] for dt in myDts if dt[0] in theirDts]
            else:
                return [dt for dt in myDts if dt[0] in theirDts]

        return execute_under_special_role(self, "Manager", doIt)

    def ensureDocTypeInTarget(self, doctype):
        """If my document type is unknown in the target ESD, copy it to the target.

        Set it to private state.

        """
        config = self.myDocumentPool().config.dtypes
        if doctype.getId() in config:
            return

        copy_id = _copyPaste(doctype, config)
        copy = config._getOb(copy_id)

        if HAS_ELAN:
            # Set intermediate category
            copy.doc_extension(ELAN_APP).setCCategory("recent")

        api.content.transition(copy, transition="retract")
        copy.reindexObject()
        copy.reindexObjectSecurity()
        config.reindexObject()

    def getSendingESD(self):
        """ """
        esd_uid = self.sendingESD
        return queryForObject(self, UID=esd_uid)

    def resetSettings(self):
        """ """
        created(self, event=None)

    def grantReadAccess(self):
        """ """

        def grantRead():
            esd = self.getSendingESD()
            prefix = esd.myPrefix()
            esd_members = "%s_Senders" % prefix
            self.myDocumentPool().manage_setLocalRoles(esd_members, ["Reader"])
            self.myDocumentPool().reindexObject()
            self.myDocumentPool().reindexObjectSecurity()

        execute_under_special_role(self, "Manager", grantRead)

    def revokeReadAccess(self):
        """ """

        def revokeRead():
            esd = self.getSendingESD()
            if esd:
                prefix = esd.myPrefix()
                esd_members = "%s_Senders" % prefix
                self.myDocumentPool().manage_delLocalRoles([esd_members])
                self.myDocumentPool().reindexObject()
                self.myDocumentPool().reindexObjectSecurity()

        execute_under_special_role(self, "Manager", revokeRead)

    def isArchive(self):
        return "archive" in self.getPhysicalPath()

    def myDPTransferFolder(self):
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

    def getDPDocuments(self, **kwargs):
        """ """
        args = {"portal_type": "DPDocument"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getFiles(self, **kwargs):
        """ """
        args = {"portal_type": "File"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getImages(self, **kwargs):
        """ """
        args = {"portal_type": "Image"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getSRModules(self, **kwargs):
        """ """
        args = {"portal_type": "SRModule"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getSituationReports(self, **kwargs):
        """ """
        args = {"portal_type": "SituationReport"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]


@adapter(IDPTransferFolder, IObjectAddedEvent)
def created(obj, event=None):
    # For all document types shared between the two ESDs
    # set the default to "publish"
    if IArchiving(obj).is_archive:
        return
    if IImportingMarker.providedBy(getRequest()):
        return
    log("TransferFolder created: %s" % str(obj))
    dts = obj.getMatchingDocumentTypes(ids_only=True)
    obj.doctypePermissions.update(dict.fromkeys(dts, "publish"))

    # Also, if the permissions include read access,
    # set the local Reader role for the members of
    # the sending ESD
    if obj.permLevel == "read/write":
        obj.grantReadAccess()


@adapter(IDPTransferFolder, IEditFinishedEvent)
def updated(obj, event=None):
    # Actually, a transfer folder should never allow a change of ESD.
    # But the permission level could have been changed. So we adapt
    # the read permissions for the sending ESD accordingly.
    log("TransferFolder updated: %s" % str(obj))

    if not IArchiving(obj).is_archive():
        if obj.permLevel == "read/write":
            obj.grantReadAccess()
        else:
            obj.revokeReadAccess()


@adapter(IDPTransferFolder, IObjectRemovedEvent)
def deleted(obj, event=None):
    log("TransferFolder deleted: %s" % str(obj))
    if not IArchiving(obj).is_archive:
        if IPloneSiteRoot.providedBy(event.object) or IDocumentPool.providedBy(
            event.object
        ):
            # do not modify content from the site or docpool that will be deleted
            return
        # Revoke any read access
        obj.revokeReadAccess()


def transfer_folders_for(obj):
    try:
        esd = obj.myDocumentPool()
    except AttributeError:
        return []

    brains = queryForObjects(
        esd, path=esd.dpSearchPath(), object_provides=IDPTransferFolder.__identifier__
    )
    return [brain.getObject() for brain in brains]


@adapter(IDocType, IObjectAddedEvent)
def doctype_added(obj, event=None):
    if IImportingMarker.providedBy(getRequest()):
        return
    dt_id = obj.getId()
    for tf in transfer_folders_for(obj):
        tf.doctypePermissions.setdefault(dt_id, "publish")


@adapter(IDocType, IObjectRemovedEvent)
def doctype_will_be_removed(obj, event=None):
    if event is None:
        return
    dt_id = obj.getId()
    for tf in transfer_folders_for(event.oldParent):
        tf.doctypePermissions.pop(dt_id, None)
