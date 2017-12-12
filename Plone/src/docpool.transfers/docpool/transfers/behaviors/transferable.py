# -*- coding: utf-8 -*-
"""Common configuration constants
"""
from docpool.base.content.dpdocument import IDPDocument
from plone.autoform.directives import read_permission, write_permission
from plone.autoform.interfaces import IFormFieldProvider
from plone.directives import form
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice, RelationList
from zope.interface import provider, implementer
from zope.component import adapter
from zope import schema
from docpool.base import DocpoolMessageFactory as _
from docpool.base.browser.flexible_view import FlexibleView
from docpool.transfers.config import TRANSFERS_APP
from five import grok
from plone.indexer.interfaces import IIndexer
from Products.ZCatalog.interfaces import IZCatalog
from Products.CMFCore.utils import getToolByName
from AccessControl import ClassSecurityInfo

from docpool.dbaccess.dbinit import __session__
from elan.esd.db.model import Channel, DocTypePermission, SenderLog, ReceiverLog,\
    ChannelSends, ChannelReceives, ChannelPermissions
from sqlalchemy import and_
from datetime import datetime
from DateTime import DateTime
from elan.esd.content.transfers import determineTransferFolderObject,\
    ensureDocTypeInTarget, ensureScenariosInTarget, determineChannels
from sqlalchemy.sql.expression import desc, or_
from docpool.base.utils import execute_under_special_role,\
    _copyPaste, getUserInfo, portalMessage

from plone import api
from Products.CMFPlone.utils import log, log_exc
from elan.esd import DocpoolMessageFactory as _
from zope.lifecycleevent.interfaces import IObjectRemovedEvent
from docpool.localbehavior.localbehavior import ILocalBehaviorSupport

from Acquisition import aq_inner
from Products.Archetypes.utils import shasattr
from docpool.base.interfaces import IDocumentExtension

@provider(IFormFieldProvider)
class ITransferable(form.Schema):
    transferred_by = schema.TextLine(
                        title=_(u'label_dpdocument_transferred_by', default=u'Transferred by'),
                        description=_(u'description_dpdocument_transferred_by', default=u''),
                        required=False,
##code-section field_transferred_by
##/code-section field_transferred_by                           
    )
    form.omitted('transferred_by')
    read_permission(transferred_by='docpool.transfers.AccessTransfers')
    write_permission(transferred_by='docpool.transfers.AccessTransfers')

    transferred = schema.Datetime(
                        title=_(u'label_dpdocument_transferred', default=u'Date of last transfer'),
                        description=_(u'description_dpdocument_transferred', default=u''),
                        required=False,
##code-section field_transferred
##/code-section field_transferred                           
    )
    form.omitted('transferred')
    read_permission(transferred='docpool.transfers.AccessTransfers')
    write_permission(transferred='docpool.transfers.AccessTransfers')

    transferLog = schema.Text(
                        title=_(u'label_dpdocument_transferlog', default=u'Transfer log'),
                        description=_(u'description_dpdocument_transferlog', default=u'Only used for archived documents.'),
                        required=False,
##code-section field_transferLog
##/code-section field_transferLog                           
    )
    form.omitted('transferLog')
    read_permission(transferLog='docpool.transfers.AccessTransfers')
    write_permission(transferLog='docpool.transfers.AccessTransfers')


class Transferable(FlexibleView):
    __allow_access_to_unprotected_subobjects__ = 1

    security = ClassSecurityInfo()

    appname = TRANSFERS_APP

    def __init__(self, context):
        self.context = context
        self.request = context.REQUEST
    
    def _get_transferred_by(self):
        return self.context.transferred_by

    def _set_transferred_by(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.transferred_by = value
    
    transferred_by = property(_get_transferred_by, _set_transferred_by)

    def _get_transferred(self):
        return getattr(self.context,'transferred', None)

    def _set_transferred(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.transferred = value
    
    transferred = property(_get_transferred, _set_transferred)

    def _get_transferLog(self):
        return self.context.transferLog

    def _set_transferLog(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.transferLog = value
    
    transferLog = property(_get_transferLog, _set_transferLog)

    def isClean(self):
        """
        Is this document free for further action like publishing or transfer.
        @return:
        """
        return True

    def changed(self):
        """
        """
        return self.context.transferred or self.context.getMdate()

    def checkTransferLog(self):
        """
        """
        return self.context.transferLog

    def transferEvents(self):
        """
        """
        if self.context.isArchive():
            return eval(self.context.transferLog)
        else:
            if self.transferred:
                # We need the receiving side
                events = __session__.query(ChannelReceives).filter(
                    ChannelReceives.document_uid == self.context.UID()).order_by(desc(ChannelReceives.etimestamp)).all()
                return [{"type": "receive", "by": event.user, "esd": event.esd_from_title,
                         "time": self.context.toLocalizedTime(DateTime(event.etimestamp), long_format=1)} for event in
                        events]
            else:
                # We need the sending side
                events = __session__.query(ChannelSends).filter(
                    ChannelSends.document_uid == self.context.UID()).order_by(desc(ChannelSends.etimestamp)).all()
                return [{"type": "send", "by": event.user, "esd": event.esd_to_title,
                         "time": self.context.toLocalizedTime(DateTime(event.etimestamp), long_format=1)} for event in
                        events]

    def transferable(self):
        """
        If not created by a transfer
        If published
        If all subobjects published (TODO: maybe they should even be transferable themselves)
        If DocType allows it
        If Object allows it directly
        """
        if not self.context.isSender():
            return False
        if self.transferred or self.context.isArchive():
            return False
        wftool = getToolByName(self.context, 'portal_workflow')
        if wftool.getInfoFor(self.context, 'review_state') != 'published':
            return False
        if not self.context.allSubobjectsPublished():
            return False
        dto = self.context.docTypeObj()
        if dto and dto.type_extension(TRANSFERS_APP).allowTransfer:
            return True
        return False

    def allowedTargets(self):
        """
        Other ESD must have allowed communication with my ESD,
        my DocType is known and must be accepted
            or the DocType is not defined in the other ESD (will be checked later)
        and my current version must not have been transferred.
        """
        esd_uid = self.context.myDocumentPool().UID()
        # print esd_uid
        dto = self.context.docTypeObj()
        dt_id = dto and dto.id or '---'
        # print dt_id
        m = self.context.getMdate()
        # print m
        q = __session__.query(Channel).outerjoin(Channel.permissions).outerjoin(Channel.sends). \
            filter(and_(Channel.esd_from_uid == esd_uid,
                        or_(and_(DocTypePermission.doc_type == dt_id,
                                 DocTypePermission.perm != 'block'),
                            ~Channel.permissions.any(DocTypePermission.doc_type == dt_id
                                                     ),
                            ),
                        ~Channel.sends.any(
                            and_(SenderLog.document_uid == self.context.UID(), SenderLog.timestamp > m)))) \
            .order_by('esd_from_title')
        # print q.statement
        targets = q.all()
        # print len(targets)
        return targets

    security.declareProtected("ELAN_E: Send Content", "transferToAll")
    def transferToAll(self):
        """
        """
        targets = self.allowedTargets()
        self.transferToTargets(targets)
        return self.context.restrictedTraverse('@@view')()

    security.declareProtected("ELAN_E: Send Content", "manage_transfer")
    def manage_transfer(self, target_ids=[]):
        """
        Performs the transfer for a list of Channel ids.
        """
        channels = determineChannels(target_ids)
        self.transferToTargets(channels)

    security.declareProtected("ELAN_E: Send Content", "transferToTargets")
    def transferToTargets(self, targets=[]):
        """
        1) Determine all transfer folder objects.
        2) Put a copy of me in each of them, preserving timestamps.
        3) Add transfer information the copies.
        4) Add log entry to sender log.
        5) If my document type is unknown in the target ESD,
           copy it to the target setting it to private state.
        6) If my scenarios are unknown in the target ESD,
           copy them to the target setting them to private state.
           If there is an equivalent scenario in the target,
           but it is in private state, check if it defines
           a published substitute scenario. If it does,
           change the scenario for the copy to that one.
        7) Add entry to receiver log.
        """
        from docpool.elan.behaviors.elandocument import IELANDocument
        from docpool.elan.config import ELAN_APP
        def doIt():
            # 1) Determine all transfer folder objects.
            for target in targets:
                transfer_folder = determineTransferFolderObject(self.context, target)
                # Check permissions:
                # a) Is my DocType accepted, are unknown DocTypes accepted?
                udt_ok = transfer_folder.unknownDtDefault != 'block'
                if not udt_ok:
                    # check my precise DocType
                    dto = self.context.docTypeObj()
                    if not transfer_folder.acceptsDT(dto.getId()):
                        portalMessage(self.context,
                                      _(u"No transfer to") + " " + target.esd_to_title + _(". Doc type not accepted."),
                                      type='error')
                        # Message
                        continue
                # b) Is my Scenario known, are unknown Scenarios accepted?
                scen_ok = transfer_folder.unknownScenDefault != 'block'
                elanobj = None
                if not scen_ok:
                    # check my precise Scenario
                    # FIXME: ELAN dependency
                    try:
                        elanobj = IELANDocument(self.context)
                    except:
                        pass # ELAN App not active
                    if elanobj != None:
                        scens = IELANDocument(self.context).myScenarioObjects()
                        if scens:
                            scen_id = scens[0].getId()
                            if not transfer_folder.knowsScen(scen_id):
                                # Message
                                portalMessage(self.context, _(u"No transfer to") + " " + target.esd_to_title + _(
                                    ". Unknown scenario not accepted."), type='error')
                                continue
                        else:
                            # Message
                            portalMessage(self.context, _(u"No transfer to") + " " + target.esd_to_title + _(
                                ". Document has no scenario."), type='error')
                            continue

                # 2) Put a copy of me in each of them, preserving timestamps.
                new_id = _copyPaste(self.context, transfer_folder)
                my_copy = transfer_folder._getOb(new_id)
                behaviors = set(ILocalBehaviorSupport(self.context).local_behaviors)
                if elanobj != None:
                    behaviors.add(ELAN_APP) # FIXME: ELAN dependency
                ILocalBehaviorSupport(my_copy).local_behaviors = list(behaviors)


                # 3) Add transfer information to the copies.
                my_copy.transferred = datetime.now()
                my_copy.transferred_by = self.context._getUserInfoString(plain=True)

                # 4) Add log entries to sender log.
                userid, fullname, primary_group = getUserInfo(self.context)
                document_uid = self.context.UID()
                document_title = self.context.Title()
                timestamp = datetime.now()
                user = userid
                scenario_ids = ""
                if elanobj != None:
                    scenario_ids = elanobj.scenarios and ", ".join(
                        elanobj.scenarios) or ""
                l = SenderLog(document_uid=document_uid,
                              document_title=document_title,
                              timestamp=timestamp,
                              user=self.context._getUserInfoString(plain=True),
                              scenario_ids=scenario_ids,
                              channel=target
                              )
                # 5) If my document type is unknown in the target ESD,
                #    copy it to the target setting it to private state.
                ensureDocTypeInTarget(self.context, my_copy)
                # 6) If my scenarios are unknown in the target ESD,
                #    copy them to the target setting them to private state.
                #    If there is an equivalent scenario in the target,
                #    but it is in private state, check if it defines
                #    a published substitute scenario. If it does,
                #    change the scenario for the copy to that one.
                if elanobj != None:
                    ensureScenariosInTarget(self.context, my_copy)
                # Make sure workflow state of the copy is published,
                # if there is no restriction on the transfer folder (permission = publish)
                # Make sure workflow state of the copy is private,
                # if permission is 'needs confirmation'
                ITransferable(my_copy).ensureState()
                my_copy.reindexObject()
                # 7) Add entry to receiver log.
                document_uid = my_copy.UID()
                document_title = my_copy.Title()
                timestamp = datetime.now()
                scenario_ids = ""
                if elanobj != None:
                    scenario_ids = IELANDocument(my_copy).scenarios and ", ".join(IELANDocument(my_copy).scenarios) or ""
                r = ReceiverLog(document_uid=document_uid,
                                document_title=document_title,
                                timestamp=timestamp,
                                user=self.context._getUserInfoString(plain=True),
                                scenario_ids=scenario_ids,
                                channel=target
                                )
                portalMessage(self.context, _(u"Transferred to") + " " + target.esd_to_title, type='info')

        execute_under_special_role(self.context, "Manager", doIt)

    def ensureState(self):
        """
        If this object is in a transfer folder,
        make sure it is in a state corresponding to the permission.
        """
        from docpool.elan.behaviors.elandocument import IELANDocument
        if self.transferred:
            tf = self.context.myELANTransferFolder()
            dtObj = self.context.docTypeObj()
            tstate = api.content.get_state(obj=dtObj)
            if tstate == 'published':  # we do this for valid types only
                # determine the applicable permission
                perm = __session__.query(ChannelPermissions).filter(ChannelPermissions.tf_uid == tf.UID(),
                                                                    ChannelPermissions.doc_type == dtObj.getId()).all()
                if perm:
                    perm = perm[0].perm
                dstate = api.content.get_state(self.context)
                if dstate == 'private' and perm == 'publish':
                    api.content.transition(self.context, 'publish')
                if dstate == 'published' and perm == 'confirm':
                    api.content.transition(self.context, 'retract')
            elanobj = None
            try:
                elanobj = IELANDocument(self.context)
            except:
                pass # no ELAN App active
            if elanobj != None:
                uscn = IELANDocument(self.context).unknownScenario()
                if uscn:
                    # Documents with unknown scenarios must be private
                    try:
                        api.content.transition(self.context, 'retract')
                    except:
                        pass

    def deleteTransferDataInDB(self):
        """
        """
        received = __session__.query(ReceiverLog).filter(ReceiverLog.document_uid == self.UID()).order_by(
            desc(ReceiverLog.timestamp)).all()
        send = __session__.query(SenderLog).filter(SenderLog.document_uid == self.UID()).order_by(
            desc(SenderLog.timestamp)).all()
        if received:
            log(received)
            for r in received:
                __session__.delete(r)
        if send:
            log(send)
            for s in send:
                __session__.delete(s)
        if received or send:
            log('received or send')
            __session__.flush()


@adapter(IDPDocument, IObjectRemovedEvent)
def deleteTransferData(obj, event=None):
    """
    # TODO: Check ob nur beim Loeschen ausgefuehrt wird oder auch beim move!?
    """
    try:
        tObj = ITransferable(obj) # Try behaviour
        log('deleteTransferData %s from %s' % (obj.Title(), obj.absolute_url()))
        tObj.deleteTransferDataInDB()
    except:
        pass
