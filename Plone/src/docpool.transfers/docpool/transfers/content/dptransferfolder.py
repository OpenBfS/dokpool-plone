# -*- coding: utf-8 -*-
#
# File: dptransferfolder.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the DPTransferFolder content type. See dptransferfolder.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from docpool.base.content.doctype import IDocType
from docpool.base.content.documentpool import IDocumentPool
from docpool.base.content.folderbase import FolderBase
from docpool.base.content.folderbase import IFolderBase
from docpool.base.utils import execute_under_special_role
from docpool.base.utils import queryForObject
from docpool.base.utils import queryForObjects
from docpool.dbaccess.dbinit import __session__
from docpool.transfers import DocpoolMessageFactory as _
from docpool.transfers.db.model import Channel
from logging import getLogger
from persistent.mapping import PersistentMapping
from plone.dexterity.content import Container
from plone.dexterity.interfaces import IEditFinishedEvent
from plone.supermodel import model
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Products.CMFPlone.utils import log
from Products.CMFPlone.utils import parent
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectRemovedEvent


logger = getLogger("dptransferfolder")


class IDPTransferFolder(model.Schema, IFolderBase):
    """
    """

    sendingESD = schema.Choice(
        title=_(
            u'label_dptransferfolder_sendingesd',
            default=u'The organisation sending content via this transfer folder',
        ),
        description=_(u'description_dptransferfolder_sendingesd', default=u''),
        required=True,
        source="docpool.base.vocabularies.DocumentPools",
    )

    permLevel = schema.Choice(
        title=_(
            u'label_dptransferfolder_permlevel',
            default=u'Permission level'),
        description=_(u'description_dptransferfolder_permlevel', default=u''),
        required=True,
        default="read/write",
        source="docpool.transfers.vocabularies.Permissions",
    )

    doctypePermissions = schema.Dict(
        title=_(
            u'label_dptransferfolder_doctypepermissions',
            default=u'Permissions by document type',
        ),
        value_type=schema.Choice(
            required=True,
            source='docpool.transfers.vocabularies.DTPermOptions',
        ),
        key_type=schema.TextLine(),
    )

    unknownDtDefault = schema.Choice(
        title=_(
            u'label_dptransferfolder_unknowndtdefault',
            default=u'Default for unknown document types',
        ),
        description=_(
            u'description_dptransferfolder_unknowndtdefault',
            default=u''),
        required=True,
        default="block",
        source="docpool.transfers.vocabularies.UnknownOptions",
    )

    unknownScenDefault = schema.Choice(
        title=_(
            u'label_dptransferfolder_unknownscendefault',
            default=u'Default for unknown scenarios',
        ),
        description=_(
            u'description_dptransferfolder_unknownscendefault',
            default=u''),
        required=True,
        default="block",
        source="docpool.transfers.vocabularies.UnknownOptions",
    )


@implementer(IDPTransferFolder)
class DPTransferFolder(Container, FolderBase):
    """
    """

    security = ClassSecurityInfo()

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.doctypePermissions = PersistentMapping()

    def migrate(self):
        f = parent(self)
        if hasattr(self, '_setPortalTypeName'):
            self._setPortalTypeName("DPTransfers")
        myid = self.getId()
        del f[myid]
        self.__class__ = DPTransferFolder
        f[myid] = self
        logger.info(self.__class__)
        logger.info(self.getPortalTypeName())

    def acceptsDT(self, dt_id):
        """
        Do I specifically accept this doc type?
        """
        perm = self.doctypePermissions.get(dt_id, False)
        return perm and perm != 'block'

    def getMatchingDocumentTypes(self, ids_only=True):
        """
        """

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

    def getSendingESD(self):
        """
        """
        esd_uid = self.sendingESD
        return queryForObject(self, UID=esd_uid)

    def resetSettings(self):
        """
        """
        created(self, event=None)

    def channelId(self):
        """
        """
        esd_from_uid = self.sendingESD
        tf_uid = self.UID()
        channel = Channel.get_by(esd_from_uid=esd_from_uid, tf_uid=tf_uid)
        if channel:
            return channel.id
        else:
            return 0

    def grantReadAccess(self):
        """
        """

        def grantRead():
            esd = self.getSendingESD()
            prefix = esd.myPrefix()
            esd_members = "%s_Senders" % prefix
            self.myDocumentPool().manage_setLocalRoles(esd_members, ["Reader"])
            self.myDocumentPool().reindexObject()
            self.myDocumentPool().reindexObjectSecurity()

        execute_under_special_role(self, "Manager", grantRead)

    def revokeReadAccess(self):
        """
        """

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
        """
        """
        return self

    def getFirstChild(self):
        """
        """
        fc = self.getFolderContents()
        if len(fc) > 0:
            return fc[0].getObject()
        else:
            return None

    def getAllContentObjects(self):
        """
        """
        return [obj.getObject() for obj in self.getFolderContents()]

    def getDPDocuments(self, **kwargs):
        """
        """
        args = {'portal_type': 'DPDocument'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getFiles(self, **kwargs):
        """
        """
        args = {'portal_type': 'File'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getImages(self, **kwargs):
        """
        """
        args = {'portal_type': 'Image'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getSRModules(self, **kwargs):
        """
        """
        args = {'portal_type': 'SRModule'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getSituationReports(self, **kwargs):
        """
        """
        args = {'portal_type': 'SituationReport'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]


def setupChannel(obj, delete=False):
    esd_from_uid = obj.sendingESD
    tf_uid = obj.UID()
    old = Channel.get_by(esd_from_uid=esd_from_uid, tf_uid=tf_uid)
    if old and delete:
        __session__.delete(old)

    if not old or delete:
        esd = obj.myDocumentPool()
        cat = getToolByName(obj, 'portal_catalog')
        from_esd = cat.unrestrictedSearchResults(
            {"portal_type": "DocumentPool", "UID": esd_from_uid}
        )
        from_esd = from_esd[0]
        c = Channel(
            esd_from_uid=esd_from_uid,
            esd_from_title=from_esd.Title,
            tf_uid=tf_uid,
            title=obj.Title(),
            esd_to_title=esd.Title(),
        )
        __session__.flush()
    else:
        c = old
    return c


@adapter(IDPTransferFolder, IObjectAddedEvent)
def created(obj, event=None):
    # Initialize all channel settings in the database.
    # For all document types shared between the two ESDs
    # set the default to "publish"
    log("TransferFolder created: %s" % str(obj))
    if not obj.restrictedTraverse("@@context_helpers").is_archive():
        dts = obj.getMatchingDocumentTypes(ids_only=True)
        obj.doctypePermissions.update(dict.fromkeys(dts, 'publish'))
        setupChannel(obj, delete=True)

        # Also, if the permissions include read access,
        # set the local Reader role for the members of
        # the sending ESD
        if obj.permLevel == 'read/write':
            obj.grantReadAccess()


@adapter(IDPTransferFolder, IEditFinishedEvent)
def updated(obj, event=None):
    # Actually, a transfer folder should never allow a change of ESD.
    # But the permission level could have been changed. So we adapt
    # the read permissions for the sending ESD accordingly.
    log("TransferFolder updated: %s" % str(obj))

    if not obj.restrictedTraverse("@@context_helpers").is_archive():
        setupChannel(obj, delete=False)

        if obj.permLevel == 'read/write':
            obj.grantReadAccess()
        else:
            obj.revokeReadAccess()


@adapter(IDPTransferFolder, IObjectRemovedEvent)
def deleted(obj, event=None):
    # Delete all channel settings from the database.
    log("TransferFolder deleted: %s" % str(obj))
    if not obj.restrictedTraverse("@@context_helpers").is_archive():
        esd_from_uid = obj.sendingESD
        tf_uid = obj.UID()
        old = Channel.get_by(esd_from_uid=esd_from_uid, tf_uid=tf_uid)
        if old:
            __session__.delete(old)
            __session__.flush()

        if IPloneSiteRoot.providedBy(event.object) or IDocumentPool.providedBy(
                event.object):
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
        esd,
        path=esd.dpSearchPath(),
        object_provides=IDPTransferFolder._identifier__
    )
    return [brain.getObject() for brain in brains]


@adapter(IDocType, IObjectAddedEvent)
def doctype_added(obj, event=None):
    dt_id = obj.getId()
    for tf in transfer_folders_for(obj):
        tf.doctypePermissions.setdefault(dt_id, 'publish')


@adapter(IDocType, IObjectRemovedEvent)
def doctype_will_be_removed(obj, event=None):
    if event is None:
        return
    dt_id = obj.getId()
    for tf in transfer_folders_for(event.oldParent):
        tf.doctypePermissions.pop(dt_id, None)


class ELANTransferFolder(DPTransferFolder):
    pass
