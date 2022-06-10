# -*- coding: utf-8 -*-
"""Common configuration constants
"""
from AccessControl import ClassSecurityInfo
from Acquisition import aq_inner
from contextlib import contextmanager
from datetime import datetime
from DateTime import DateTime
from docpool.base.browser.flexible_view import FlexibleView
from docpool.base.content.dpdocument import IDPDocument
from docpool.base.utils import _copyPaste
from docpool.base.utils import execute_under_special_role
from docpool.base.utils import portalMessage
from docpool.localbehavior.localbehavior import ILocalBehaviorSupport
from docpool.transfers import DocpoolMessageFactory as _
from docpool.transfers.config import TRANSFERS_APP
from docpool.transfers.content.transfers import ensureDocTypeInTarget
from docpool.transfers.db.query import allowed_targets
from docpool.transfers.utils import is_sender
from logging import getLogger
from plone import api
from plone.autoform import directives
from plone.autoform.directives import read_permission
from plone.autoform.directives import write_permission
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from Products.CMFCore.interfaces import IActionSucceededEvent
from Products.CMFCore.utils import getToolByName
from Products.statusmessages.interfaces import IStatusMessage
from sqlalchemy.exc import SQLAlchemyError
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.globalrequest import getRequest
from zope.interface import provider


logger = getLogger(__name__)

ANNOTATIONS_KEY = __name__


@contextmanager
def transferring():
    """Keeps record of a tranfer going on while the code block executes.

    The resource returned is a boolean telling whether a transfer was already going on
    when entering the code block.

    """
    annotations = IAnnotations(getRequest()).setdefault(ANNOTATIONS_KEY, {})
    KEY = 'transferring'
    if annotations.get(KEY, False):
        yield True
    else:
        annotations[KEY] = True
        try:
            yield False
        finally:
            del annotations[KEY]


@provider(IFormFieldProvider)
class ITransferable(model.Schema):
    transferred_by = schema.TextLine(
        title=_(u'label_dpdocument_transferred_by', default=u'Transferred by'),
        description=_(u'description_dpdocument_transferred_by', default=u''),
        required=False,
    )
    directives.omitted('transferred_by')
    read_permission(transferred_by='docpool.transfers.AccessTransfers')
    write_permission(transferred_by='docpool.transfers.AccessTransfers')

    transferred = schema.Datetime(
        title=_(
            u'label_dpdocument_transferred',
            default=u'Date of last transfer'),
        description=_(u'description_dpdocument_transferred', default=u''),
        required=False,
    )
    directives.omitted('transferred')
    read_permission(transferred='docpool.transfers.AccessTransfers')
    write_permission(transferred='docpool.transfers.AccessTransfers')

    transferLog = schema.Text(
        title=_(u'label_dpdocument_transferlog', default=u'Transfer log'),
        description=_(
            u'description_dpdocument_transferlog',
            default=u'Only used for archived documents.',
        ),
        required=False,
    )
    directives.omitted('transferLog')
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
        return getattr(self.context, 'transferred', None)

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

    @property
    def sender_log(self):
        return getattr(self.context, 'transfer_sender_log', ())

    @sender_log.setter
    def sender_log(self, value):
        context = aq_inner(self.context)
        context.transfer_sender_log = value

    @property
    def receiver_log(self):
        return getattr(self.context, 'transfer_receiver_log', ())

    @receiver_log.setter
    def receiver_log(self, value):
        context = aq_inner(self.context)
        context.transfer_receiver_log = value

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
        try:
            return self._transferEvents()
        except SQLAlchemyError:
            msg = 'Es ist ein Fehler aufgetreten. Bitte laden Sie die Seite neu.'
            IStatusMessage(self.request).add(msg, 'error')
            return ()

    def _transferEvents(self):
        """Query metadata of past transfers ("transfer events") of the context object.
        """
        if self.context.restrictedTraverse("@@context_helpers").is_archive():
            logRaw = self.context.transferLog
            logRaw = logRaw and logRaw.replace(
                "datetime.datetime", "datetime") or ""
            return eval(logRaw)

        else:
            if self.transferred:
                type_ = 'receive'
                events = reversed(self.context.receiver_log)
            else:
                type_ = 'send'
                events = reversed(self.context.sender_log)
                return [
                    {
                        "type": type_,
                        "by": event['user'],
                        "esd": event['esd_title'],
                        "timeraw": event['timestamp'],
                        "time": self.context.toLocalizedTime(
                            DateTime(event['timestamp']), long_format=1
                        ),
                    }
                    for event in events
                ]

    def transferable(self):
        """
        If not created by a transfer
        If published
        If all subobjects published (TODO: maybe they should even be transferable themselves)
        If DocType allows it
        If Object allows it directly
        """
        if not is_sender(self.context):
            return False
        if self.transferred or self.context.restrictedTraverse("@@context_helpers").is_archive():
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
        return allowed_targets(self.context)

    security.declareProtected("Docpool: Send Content", "transferToAll")

    def transferToAll(self):
        """
        """
        dto = self.context.docTypeObj()
        dto_transfers = dto.type_extension(TRANSFERS_APP)
        # Intersect allowed and automatic transfer targets while keeping the order of
        # allowed targets and computing the automatic ones only once.
        automatic = set(dto_transfers.automaticTransferTargets)
        targets = [t.tf_uid for t in self.allowedTargets() if t.tf_uid in automatic]

        source_path = '/'.join(self.context.getPhysicalPath())
        if targets:
            logger.info(
                'Transfer {} to up to {} targets.'.format(source_path, len(targets))
            )
            self.transferToTargets(targets)
        else:
            logger.info('No transfer targets found for {}.'.format(source_path))

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
        HAS_ELAN = True
        try:
            from docpool.elan.behaviors.elandocument import IELANDocument
            from docpool.elan.config import ELAN_APP
            from docpool.elan.content.transfers import (
                ensureScenariosInTarget,
                knowsScen,
            )
        except BaseException:
            HAS_ELAN = False

        def doIt():
            timestamp = datetime.now()
            userinfo_string = self.context._getUserInfoString(plain=True)

            # 1) Determine all transfer folder objects.
            for target in targets:
                transfer_folder = api.content.get(UID=target)
                esd_to_title = transfer_folder.myDocumentPool().Title()
                # Check permissions:
                # a) Is my DocType accepted, are unknown DocTypes accepted?
                udt_ok = transfer_folder.unknownDtDefault != 'block'
                if not udt_ok:
                    # check my precise DocType
                    dto = self.context.docTypeObj()
                    if not transfer_folder.acceptsDT(dto.getId()):
                        portalMessage(
                            self.context,
                            _(u"No transfer to")
                            + " "
                            + esd_to_title
                            + _(". Doc type not accepted."),
                            type='error',
                        )
                        # Message
                        continue
                # b) Is my Scenario known, are unknown Scenarios accepted?
                scen_ok = transfer_folder.unknownScenDefault != 'block'
                elanobj = None
                if not scen_ok and HAS_ELAN:
                    # check my precise Scenario
                    # FIXME: ELAN dependency
                    try:
                        elanobj = IELANDocument(self.context)
                    except BaseException:
                        pass  # ELAN App not active
                    if elanobj is not None:
                        scens = IELANDocument(self.context).myScenarioObjects()
                        if scens:
                            scen_id = scens[0].getId()
                            if not knowsScen(transfer_folder, scen_id):
                                # Message
                                portalMessage(
                                    self.context,
                                    _(u"No transfer to")
                                    + " "
                                    + esd_to_title
                                    + _(". Unknown scenario not accepted."),
                                    type='error',
                                )
                                continue
                        else:
                            # Message
                            portalMessage(
                                self.context,
                                _(u"No transfer to")
                                + " "
                                + esd_to_title
                                + _(". Document has no scenario."),
                                type='error',
                            )
                            continue

                logger.info(
                    'Transfer {} to {}.'.format(
                        '/'.join(self.context.getPhysicalPath()),
                        esd_to_title,
                    )
                )

                # 2) Put a copy of me in each of them, preserving timestamps.
                new_id = _copyPaste(self.context, transfer_folder)
                my_copy = transfer_folder._getOb(new_id)
                behaviors = set(
                    ILocalBehaviorSupport(
                        self.context).local_behaviors)
                if HAS_ELAN and elanobj is not None:
                    behaviors.add(ELAN_APP)  # FIXME: ELAN dependency
                ILocalBehaviorSupport(
                    my_copy).local_behaviors = list(set(behaviors))

                # 3) Add transfer information to the copies.
                my_copy.transferred = timestamp
                my_copy.transferred_by = userinfo_string

                # 4) Add log entries to sender log.
                scenario_ids = ""
                if HAS_ELAN and elanobj is not None:
                    scenario_ids = (
                        elanobj.scenarios and ", ".join(
                            elanobj.scenarios) or ""
                    )
                self.sender_log += (
                    dict(
                        timestamp=timestamp,
                        user=userinfo_string,
                        scenario_ids=scenario_ids,
                        esd_title=esd_to_title,
                        transferfolder_uid=transfer_folder.UID(),
                    ),
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
                if HAS_ELAN and elanobj is not None:
                    ensureScenariosInTarget(self.context, my_copy)
                # Make sure workflow state of the copy is published,
                # if there is no restriction on the transfer folder (permission = publish)
                # Make sure workflow state of the copy is private,
                # if permission is 'needs confirmation'
                ITransferable(my_copy).ensureState()
                my_copy.reindexObject()
                # 7) Add entry to receiver log.
                scenario_ids = ""
                if elanobj is not None:
                    scenario_ids = (
                        IELANDocument(my_copy).scenarios
                        and ", ".join(IELANDocument(my_copy).scenarios)
                        or ""
                    )
                self.receiver_log += (
                    dict(
                        timestamp=timestamp,
                        user=userinfo_string,
                        scenario_ids=scenario_ids,
                        esd_title=target.getSendingESD().Title(),
                    ),
                )
                msg = _('Transferred to ${target_title}', mapping={'target_title': esd_to_title})
                api.portal.show_message(msg, self.request)

        execute_under_special_role(self.context, "Manager", doIt)

    def ensureState(self):
        """
        If this object is in a transfer folder,
        make sure it is in a state corresponding to the permission.
        """
        HAS_ELAN = True
        try:
            from docpool.elan.behaviors.elandocument import IELANDocument
        except BaseException:
            HAS_ELAN = False
        if self.transferred:
            tf = self.context.myDPTransferFolder()
            dtObj = self.context.docTypeObj()
            tstate = api.content.get_state(obj=dtObj)
            if tstate == 'published':  # we do this for valid types only
                # determine the applicable permission
                perm = tf.doctypePermissions.get(dtObj.getId())
                dstate = api.content.get_state(self.context)
                if dstate == 'private' and perm == 'publish':
                    api.content.transition(self.context, 'publish')
                if dstate == 'published' and perm == 'confirm':
                    api.content.transition(self.context, 'retract')
            if HAS_ELAN:
                elanobj = None
                try:
                    elanobj = IELANDocument(self.context)
                except BaseException:
                    pass  # no ELAN App active
                if elanobj is not None:
                    uscn = IELANDocument(self.context).unknownScenario()
                    if uscn:
                        # Documents with unknown scenarios must be private
                        try:
                            api.content.transition(self.context, 'retract')
                        except BaseException:
                            pass


@adapter(IDPDocument, IActionSucceededEvent)
def automatic_transfer_on_publish(obj, event=None):
    """
    """
    if event and event.action == 'publish':
        automatic_transfer(obj)


def automatic_transfer(obj):
    if obj.restrictedTraverse("@@context_helpers").is_archive():
        # In the process of archiving an event, its associated documents are copied and
        # afterwards applied a workflow transition in order to restore their original
        # workflow state. Objects published for this reason should not be transferred.
        return

    try:
        tObj = ITransferable(obj)  # Try behaviour
    except BaseException:
        return

    with transferring() as already_transferring:
        if already_transferring:
            return

        logger.info(
            'Automatic transfer of "{}" from {}'.format(
                obj.Title(),
                '/'.join(obj.getPhysicalPath()),
            )
        )
        try:
            return tObj.transferToAll()
        except BaseException:
            pass
