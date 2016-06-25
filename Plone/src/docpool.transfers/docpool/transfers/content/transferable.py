# -*- coding: utf-8 -*-
#
# File: transferable.py
#
# Copyright (c) 2016 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the Transferable content type. See transferable.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from zope.interface import implements
from zope.component import adapts
from zope import schema
from plone.directives import form, dexterity
from plone.app.textfield import RichText
from plone.namedfile.field import NamedBlobImage
from collective import dexteritytextindexer
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder
from Products.CMFPlone.utils import log, log_exc

from plone.dexterity.content import Item
from docpool.base.content.documentextension import DocumentExtension, IDocumentExtension

from Products.CMFCore.utils import getToolByName

##code-section imports
from docpool.transfers.config import TRANSFERS_APP
from elan.dbaccess.dbinit import __session__
from DateTime import DateTime
from datetime import datetime
from sqlalchemy.sql.expression import desc, or_, and_
from docpool.base.utils import execute_under_special_role, \
    _copyPaste, getUserInfo, portalMessage
from plone import api
from zope.component import adapter
from Products.Archetypes.utils import shasattr
from zope.lifecycleevent import IObjectRemovedEvent

from docpool.elan.config import ELAN_APP
from elan.esd.content.transfers import determineChannels, determineTransferFolderObject, ensureDocTypeInTarget, \
    ensureScenariosInTarget
from elan.esd.db.model import ChannelReceives, ChannelSends, Channel, DocTypePermission, SenderLog, ReceiverLog, \
    ChannelPermissions
##/code-section imports 

from docpool.transfers.config import PROJECTNAME

from docpool.transfers import DocpoolMessageFactory as _

class ITransferable(form.Schema, IDocumentExtension):
    """
    """

##code-section interface
    transferred_by = schema.TextLine(
        title=_(u'label_dpdocument_transferred_by', default=u'Transferred by'),
        description=_(u'description_dpdocument_transferred_by', default=u''),
        required=False,
        ##code-section field_transferred_by
        ##/code-section field_transferred_by
    )


    form.omitted('transferred_by')

    transferred = schema.Datetime(
        title=_(u'label_dpdocument_transferred', default=u'Date of last transfer'),
        description=_(u'description_dpdocument_transferred', default=u''),
        required=False,
        ##code-section field_transferred
        ##/code-section field_transferred
    )
    form.omitted('transferred')

    transferLog = schema.Text(
        title=_(u'label_dpdocument_transferlog', default=u'Transfer log'),
        description=_(u'description_dpdocument_transferlog', default=u'Only used for archived documents.'),
        required=False,
        ##code-section field_transferLog
        ##/code-section field_transferLog
    )
    form.omitted('transferLog')


##/code-section interface


class Transferable(Item, DocumentExtension):
    """
    """
    security = ClassSecurityInfo()
    
    implements(ITransferable)
    
##code-section methods
    def changed(self):
        """
        """
        return self.transferred or self.getMdate()


    def checkTransferLog(self):
        """
        """
        return self.transferLog


    def transferEvents(self):
        """
        """
        if self.isArchive():
            return eval(self.transferLog)
        else:
            if self.transferred:
                # We need the receiving side
                events = __session__.query(ChannelReceives).filter(
                    ChannelReceives.document_uid == self.contextObject().UID()).order_by(desc(ChannelReceives.etimestamp)).all()
                return [{"type": "receive", "by": event.user, "esd": event.esd_from_title,
                         "time": self.toLocalizedTime(DateTime(event.etimestamp), long_format=1)} for event in
                        events]
            else:
                # We need the sending side
                events = __session__.query(ChannelSends).filter(ChannelSends.document_uid == self.contextObject().UID()).order_by(
                    desc(ChannelSends.etimestamp)).all()
                return [{"type": "send", "by": event.user, "esd": event.esd_to_title,
                         "time": self.toLocalizedTime(DateTime(event.etimestamp), long_format=1)} for event in
                        events]


    def transferable(self):
        """
        If not created by a transfer
        If published
        If DocType allows it
        If Object allows it directly
        """
        if not self.isSender():
            return False
        if self.transferred or self.isArchive():
            return False
        wftool = getToolByName(self, 'portal_workflow')
        if wftool.getInfoFor(self.contextObject(), 'review_state') != 'published':
            return False
        dto = self.docTypeObj()
        # We know that the app is avaible because we are in a TRANSFERS extension object
        if dto and dto.extension(TRANSFERS_APP).allowTransfer:
            return True
        if shasattr(self.contextObject(), "transferable"):
            return self.contextObject().transferable()
        return False


    def allowedTargets(self):
        """
        Other ESD must have allowed communication with my ESD,
        my DocType is known and must be accepted
            or the DocType is not defined in the other ESD (will be checked later)
        and my current version must not have been transferred.
        """
        esd_uid = self.myDocumentPool().UID()
        print esd_uid
        dto = self.docTypeObj()
        dt_id = dto and dto.id or '---'
        print dt_id
        m = self.getMdate()
        # print m
        q = __session__.query(Channel).outerjoin(Channel.permissions).outerjoin(Channel.sends). \
            filter(and_(Channel.esd_from_uid == esd_uid,
                        or_(and_(DocTypePermission.doc_type == dt_id,
                                 DocTypePermission.perm != 'block'),
                            ~Channel.permissions.any(DocTypePermission.doc_type == dt_id
                                                     ),
                            ),
                        ~Channel.sends.any(and_(SenderLog.document_uid == self.contextObject().UID(), SenderLog.timestamp > m)))) \
            .order_by('esd_from_title')
        # print q.statement
        targets = q.all()
        # print len(targets)
        return targets


    security.declareProtected("Docpool: Send Content", "transferToAll")


    def transferToAll(self):
        """
        """
        targets = self.allowedTargets()
        self.transferToTargets(targets)
        return self.contextObject().restrictedTraverse('@@view')()


    security.declareProtected("Docpool: Send Content", "manage_transfer")


    def manage_transfer(self, target_ids=[]):
        """
        Performs the transfer for a list of Channel ids.
        """
        channels = determineChannels(target_ids)
        self.transferToTargets(channels)


    security.declareProtected("Docpool: Send Content", "transferToTargets")


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
        from elan.esd.behaviors.elandocument import IELANDocument
        def doIt():
            # 1) Determine all transfer folder objects.
            for target in targets:
                transfer_folder = determineTransferFolderObject(self, target)
                # Check permissions:
                # a) Is my DocType accepted, are unknown DocTypes accepted?
                udt_ok = transfer_folder.unknownDtDefault != 'block'
                if not udt_ok:
                    # check my precise DocType
                    dto = self.docTypeObj()
                    if not transfer_folder.acceptsDT(dto.getId()):
                        portalMessage(self,
                                      _(u"No transfer to") + " " + target.esd_to_title + _(". Doc type not accepted."),
                                      type='error')
                        # Message
                        continue
                # b) Is my Scenario known, are unknown Scenarios accepted?
                scen_ok = transfer_folder.unknownScenDefault != 'block'
                if not scen_ok:
                    # check my precise Scenario
                    scens = self.contextObject().extension(ELAN_APP).myScenarioObjects()
                    if scens:
                        scen_id = scens[0].getId()
                        if not transfer_folder.knowsScen(scen_id):
                            # Message
                            portalMessage(self, _(u"No transfer to") + " " + target.esd_to_title + _(
                                ". Unknown scenario not accepted."), type='error')
                            continue
                    else:
                        # Message
                        portalMessage(self,
                                      _(u"No transfer to") + " " + target.esd_to_title + _(". Document has no scenario."),
                                      type='error')
                        continue

                # 2) Put a copy of me in each of them, preserving timestamps.
                new_id = _copyPaste(self.contextObject(), transfer_folder)
                my_copy = transfer_folder._getOb(new_id)

                # 3) Add transfer information to the copies.
                my_copy.transferred = datetime.now()
                my_copy.transferred_by = self._getUserInfoString()

                # 4) Add log entries to sender log.
                userid, fullname, primary_group = getUserInfo(self.contextObject())
                document_uid = self.contextObject().UID()
                document_title = self.contextObject().Title()
                timestamp = datetime.now()
                user = userid
                scenario_ids = self.contextObject().extension(ELAN_APP).scenarios and ", ".join(
                    self.contextObject().extension(ELAN_APP).scenarios) or ""
                l = SenderLog(document_uid=document_uid,
                              document_title=document_title,
                              timestamp=timestamp,
                              user=self.contextObject()._getUserInfoString(),
                              scenario_ids=scenario_ids,
                              channel=target
                              )
                # 5) If my document type is unknown in the target ESD,
                #    copy it to the target setting it to private state.
                ensureDocTypeInTarget(self.contextObject(), my_copy)
                # 6) If my scenarios are unknown in the target ESD,
                #    copy them to the target setting them to private state.
                #    If there is an equivalent scenario in the target,
                #    but it is in private state, check if it defines
                #    a published substitute scenario. If it does,
                #    change the scenario for the copy to that one.
                ensureScenariosInTarget(self.contextObject(), my_copy)
                # Make sure workflow state of the copy is published,
                # if there is no restriction on the transfer folder (permission = publish)
                # Make sure workflow state of the copy is private,
                # if permission is 'needs confirmation'
                my_copy.extension(TRANSFERS_APP).ensureState()
                my_copy.reindexObject()
                # 7) Add entry to receiver log.
                document_uid = my_copy.UID()
                document_title = my_copy.Title()
                timestamp = datetime.now()
                scenario_ids = my_copy.extension(ELAN_APP).scenarios and ", ".join(my_copy.extension(ELAN_APP).scenarios) or ""
                r = ReceiverLog(document_uid=document_uid,
                                document_title=document_title,
                                timestamp=timestamp,
                                user=self.contextObject()._getUserInfoString(),
                                scenario_ids=scenario_ids,
                                channel=target
                                )
                portalMessage(self, _(u"Transferred to") + " " + target.esd_to_title, type='info')

        execute_under_special_role(self, "Manager", doIt)


    def ensureState(self):
        """
        If this object is in a transfer folder,
        make sure it is in a state corresponding to the permission.
        """
        from elan.esd.behaviors.elandocument import IELANDocument
        if self.transferred:
            tf = self.myELANTransferFolder()
            dtObj = self.docTypeObj()
            tstate = api.content.get_state(obj=dtObj)
            if tstate == 'published':  # we do this for valid types only
                # determine the applicable permission
                perm = __session__.query(ChannelPermissions).filter(ChannelPermissions.tf_uid == tf.UID(),
                                                                    ChannelPermissions.doc_type == dtObj.getId()).all()
                if perm:
                    perm = perm[0].perm
                dstate = api.content.get_state(self.contextObject())
                if dstate == 'private' and perm == 'publish':
                    api.content.transition(self.contextObject(), 'publish')
                if dstate == 'published' and perm == 'confirm':
                    api.content.transition(self.contextObject(), 'retract')
            uscn = self.contextObject().extension(ELAN_APP).unknownScenario()
            if uscn:
                # Documents with unknown scenarios must be private
                try:
                    api.content.transition(self.contextObject(), 'retract')
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

##/code-section methods 


##code-section bottom
@adapter(ITransferable, IObjectRemovedEvent)
def deleteTransferData(obj, event=None):
    """
    """
    #TODO: Check ob nur beim Loeschen ausgefuehrt wird oder auch beim move!?
    log('deleteTransferData %s from %s' % (obj.Title(), obj.absolute_url()))
    obj.deleteTransferDataInDB()
##/code-section bottom 
