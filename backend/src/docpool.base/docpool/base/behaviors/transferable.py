from AccessControl import ClassSecurityInfo
from Acquisition import aq_inner
from contextlib import contextmanager
from DateTime import DateTime
from datetime import datetime
from docpool.base import DocpoolMessageFactory as _
from docpool.base.behaviors.transferstype import ITransfersType
from docpool.base.behaviors.utils import allowed_targets
from docpool.base.browser.flexible_view import FlexibleView
from docpool.base.config import TRANSFERS_APP
from docpool.base.content.archiving import IArchiving
from docpool.base.content.dpdocument import IDPDocument
from docpool.base.localbehavior.localbehavior import ILocalBehaviorSupport
from docpool.base.marker import IImportingMarker
from docpool.base.utils import _copyPaste
from docpool.base.utils import ContextProperty
from docpool.base.utils import execute_under_special_role
from docpool.base.utils import portalMessage
from logging import getLogger
from plone import api
from plone.autoform import directives
from plone.autoform.directives import read_permission
from plone.autoform.directives import write_permission
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from Products.CMFCore.interfaces import IActionSucceededEvent
from Products.CMFPlone.utils import log
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.component import queryMultiAdapter
from zope.globalrequest import getRequest
from zope.interface import Interface
from zope.interface import provider

import logging


logger = getLogger(__name__)

ANNOTATIONS_KEY = __name__


@contextmanager
def transferring():
    """Keeps record of a tranfer going on while the code block executes.

    The resource returned is a boolean telling whether a transfer was already going on
    when entering the code block.

    """
    annotations = IAnnotations(getRequest()).setdefault(ANNOTATIONS_KEY, {})
    KEY = "transferring"
    if annotations.get(KEY, False):
        yield True
    else:
        annotations[KEY] = True
        try:
            yield False
        finally:
            del annotations[KEY]


class ISkipAutomaticTransferMarker(Interface):
    """Marker interface for containers whose content should be ignored for automatic transfers."""


class IAppSpecificTransfer(Interface):
    pass


@provider(IFormFieldProvider)
class ITransferable(model.Schema):
    transferred_by = schema.TextLine(
        title=_("label_dpdocument_transferred_by", default="Transferred by"),
        description=_("description_dpdocument_transferred_by", default=""),
        required=False,
    )
    directives.omitted("transferred_by")
    read_permission(transferred_by="docpool.transfers.AccessTransfers")
    write_permission(transferred_by="docpool.transfers.AccessTransfers")

    transferred = schema.Datetime(
        title=_("label_dpdocument_transferred", default="Date of last transfer"),
        description=_("description_dpdocument_transferred", default=""),
        required=False,
    )
    directives.omitted("transferred")
    read_permission(transferred="docpool.transfers.AccessTransfers")
    write_permission(transferred="docpool.transfers.AccessTransfers")

    transferLog = schema.Text(
        title=_("label_dpdocument_transferlog", default="Transfer log"),
        description=_("description_dpdocument_transferlog", default="Only used for archived documents."),
        required=False,
    )
    directives.omitted("transferLog")
    read_permission(transferLog="docpool.transfers.AccessTransfers")
    write_permission(transferLog="docpool.transfers.AccessTransfers")


class Transferable(FlexibleView):
    __allow_access_to_unprotected_subobjects__ = 1

    security = ClassSecurityInfo()

    appname = "transfers"

    def __init__(self, context):
        self.context = context
        self.request = context.REQUEST

    transferred_by = ContextProperty("transferred_by", skip_empty=True)
    transferred = ContextProperty("transferred", skip_empty=True)
    transferLog = ContextProperty("transferLog", skip_empty=True)

    @property
    def sender_log(self):
        return getattr(self.context, "transfer_sender_log", ())

    @sender_log.setter
    def sender_log(self, value):
        context = aq_inner(self.context)
        context.transfer_sender_log = value

    @property
    def receiver_log(self):
        return getattr(self.context, "transfer_receiver_log", ())

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
        """ """
        return self.context.transferred or self.context.getMdate()

    def checkTransferLog(self):
        """ """
        return self.context.transferLog

    def transferEvents(self):
        """Query metadata of past transfers ("transfer events") of the context object."""
        if IArchiving(self.context).is_archive:
            logRaw = self.transferLog
            logRaw = logRaw and logRaw.replace("datetime.datetime", "datetime")
            return eval(logRaw) if logRaw else None

        else:
            if self.transferred:
                type_ = "receive"
                events = reversed(self.receiver_log)
            else:
                type_ = "send"
                events = reversed(self.sender_log)
            plone_view = api.content.get_view("plone", self.context, self.request)
            return [
                {
                    "type": type_,
                    "by": event["user"],
                    "esd": event["esd_title"],
                    "timeraw": event["timestamp"],
                    "time": plone_view.toLocalizedTime(DateTime(event["timestamp"]), long_format=1),
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
        if self.transferred or IArchiving(self.context).is_archive:
            return False
        if api.content.get_state(obj=self.context, default=None) != "published":
            return False
        if not self.context.allSubobjectsPublished():
            return False
        dto = self.context.docTypeObj()
        if dto and ITransfersType(dto).allowTransfer:
            return True
        return False

    def allowedTargets(self):
        return [i["uid"] for i in allowed_targets(self.context)]

    security.declareProtected("Docpool: Send Content", "transferToAll")

    def transferToAll(self):
        """ """
        dto = self.context.docTypeObj()
        dto_transfers = dto.type_extension(TRANSFERS_APP)
        # Intersect allowed and automatic transfer targets while keeping the order of
        # allowed targets and computing the automatic ones only once.
        automatic = set(dto_transfers.automaticTransferTargets)
        targets = [t for t in self.allowedTargets() if t in automatic]

        source_path = "/".join(self.context.getPhysicalPath())
        if targets:
            logger.info(f"Transfer {source_path} to up to {len(targets)} targets.")
            self.transferToTargets(targets)
        else:
            logger.info(f"No transfer targets found for {source_path}.")

    security.declareProtected("Docpool: Send Content", "transferToTargets")

    def transferToTargets(self, targets=None):
        """
        1) Determine all transfer folder objects.
        2) Put a copy of me in each of them, preserving timestamps.
        3) Add transfer information the copies.
        4) Add entries to sender logs.
        5) Make sure about document type in the target ESD.
        6) Apply app-specific transfer steps.
        7) Set workflow state of the copies according to folder permissions.
        8) Add entries to receiver logs.
        """

        if targets is None:
            return

        catalog = api.portal.get_tool("portal_catalog")
        scenarios_index = catalog._catalog.getIndex("scenarios")
        timestamp = datetime.now()
        userinfo_string = self.context._getUserInfoString(plain=True)
        dto = self.context.docTypeObj()

        def error_message(esd_to_title, msg):
            pmsg = _("No transfer to ${title}. ${msg}", mapping=dict(title=esd_to_title, msg=msg))
            portalMessage(self.context, pmsg, type="error")

        def doIt():
            # TODO The idea of this function is to avoid executing do_target multiple times under the manager
            # role but if performance turns out not to be an issue, the loop might be done by the outer method
            # directly.
            for target in targets:
                do_target(target)

        def do_target(target):
            # 1) Determine target transfer folder object.
            transfer_folder = api.content.get(UID=target)
            esd_to_title = transfer_folder.myDocumentPool().Title()

            # Check permissions:
            # a) Is my DocType accepted, are unknown DocTypes accepted?
            udt_ok = transfer_folder.unknownDtDefault != "block"
            if not udt_ok:
                # check my precise DocType
                if not transfer_folder.acceptsDT(dto.getId()):
                    error_message(esd_to_title, _("Doc type not accepted."))
                    return

            # Collect transfer specifics for apps supported by both original and target.
            app_transfers = []
            apps_to_remove = set()
            for app in (lbs := ILocalBehaviorSupport(self.context)).local_behaviors:
                if app not in transfer_folder.myDocumentPool().supportedApps:
                    apps_to_remove.add(app)
                    continue
                app_transfer = queryMultiAdapter(
                    (self.context, transfer_folder), IAppSpecificTransfer, name=app
                )
                if app_transfer is not None:
                    app_transfers.append(app_transfer)

            # b) Check app-specific conditions that might deny transfer.
            for app_transfer in app_transfers:
                try:
                    app_transfer.assert_allowed()
                except BaseException as exc:
                    error_message(esd_to_title, exc.args[0])
                    return

            # At this point, transfer is allowed.
            logger.info(f"Transfer {'/'.join(self.context.getPhysicalPath())} to {esd_to_title}.")

            # 2) Put a copy of me in transfer folder, preserving timestamps.
            new_id = _copyPaste(self.context, transfer_folder)
            my_copy = transfer_folder._getOb(new_id)

            # 3) Add transfer information to the copies.
            my_copy.transferred = timestamp
            my_copy.transferred_by = userinfo_string

            # 4) Add entry to sender log.
            log_entry = dict(
                timestamp=timestamp,
                user=userinfo_string,
                esd_title=esd_to_title,
                transferfolder_uid=transfer_folder.UID(),
            )
            for app_transfer in app_transfers:
                log_entry.update(app_transfer.sender_log_entry())
            self.sender_log += (log_entry,)

            # 5) Make sure about document type in the target ESD.
            private = False
            if not my_copy.docTypeObj():
                my_copy.docType = "none"
                private = True

            # 6) Apply app-specific transfer steps.
            ILocalBehaviorSupport(my_copy).local_behaviors = set(lbs.local_behaviors) - apps_to_remove
            for app_transfer in app_transfers:
                app_transfer(my_copy)

            # 7) Set workflow state of the copy according to folder permissions.
            transfer_copy = ITransferable(my_copy)
            transfer_copy.ensureState(private)
            my_copy.reindexObject()

            # 8) Add entry to receiver log.
            log_entry = dict(
                timestamp=timestamp,
                user=userinfo_string,
                esd_title=transfer_folder.getSendingESD().Title(),
            )
            for app_transfer in app_transfers:
                log_entry.update(app_transfer.receiver_log_entry())
            transfer_copy.receiver_log += (log_entry,)

            msg = _("Transferred to ${target_title}", mapping={"target_title": esd_to_title})
            api.portal.show_message(msg, self.request)

            brain = api.content.find(UID=my_copy.UID())[0]
            index_entry = scenarios_index.getEntryForObject(brain.getRID(), [])
            if set(getattr(my_copy, "scenarios", [])) != set(index_entry):
                log(
                    f"Inconsistent scenarios index for {'/'.join(my_copy.getPhysicalPath())}",
                    severity=logging.ERROR,
                )

        execute_under_special_role(self.context, "Manager", doIt)

    def ensureState(self, private=False):
        """Put a transferred object in a state corresponding to the doctype permission.

        If there is no restriction on the transfer folder (permission is 'publish'),
        make sure workflow state of the copy is private if permission is 'needs
        confirmation' but public if it is 'publish'.

        Allow override if there is a reason to make sure the document is private under
        any condition.

        """
        if private:
            if api.content.get_state(self.context) != "private":
                api.content.transition(self.context, "retract")
            return

        if self.transferred:
            tf = self.context.myDPTransferFolder()
            dtObj = self.context.docTypeObj()
            tstate = api.content.get_state(obj=dtObj)
            if tstate == "published":  # we do this for valid types only
                # determine the applicable permission
                perm = tf.doctype_permission(dtObj.getId())
                dstate = api.content.get_state(self.context)
                if dstate == "private" and perm == "publish":
                    api.content.transition(self.context, "publish")
                if dstate == "published" and perm == "confirm":
                    api.content.transition(self.context, "retract")


@adapter(IDPDocument, IActionSucceededEvent)
def automatic_transfer_on_publish(obj, event=None):
    """ """
    if event and event.action == "publish":
        automatic_transfer(obj)


def automatic_transfer(obj):
    if IArchiving(obj).is_archive:
        # In the process of archiving an event, its associated documents are copied and
        # afterwards applied a workflow transition in order to restore their original
        # workflow state. Objects published for this reason should not be transferred.
        return
    if IImportingMarker.providedBy(getRequest()):
        return
    if ISkipAutomaticTransferMarker.providedBy(obj.__parent__):
        return

    try:
        tObj = ITransferable(obj)  # Try behaviour
    except BaseException:
        return

    with transferring() as already_transferring:
        if already_transferring:
            return

        logger.info(f'Automatic transfer of "{obj.Title()}" from {"/".join(obj.getPhysicalPath())}')
        try:
            return tObj.transferToAll()
        except BaseException:
            pass


def is_sender(obj):
    roles = api.user.get_roles(obj=obj)
    if "Manager" in roles or "Site Administrator" in roles or "ContentSender" in roles:
        return True
    return any("Senders" in group for group in api.user.get_current().getGroups())
