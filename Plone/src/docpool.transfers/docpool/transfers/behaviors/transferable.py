from AccessControl import ClassSecurityInfo
from Acquisition import aq_inner
from contextlib import contextmanager
from datetime import datetime
from DateTime import DateTime
from docpool.base.browser.flexible_view import FlexibleView
from docpool.base.content.archiving import IArchiving
from docpool.base.content.dpdocument import IDPDocument
from docpool.base.localbehavior.localbehavior import ILocalBehaviorSupport
from docpool.base.marker import IImportingMarker
from docpool.base.utils import _copyPaste
from docpool.base.utils import execute_under_special_role
from docpool.base.utils import portalMessage
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
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.globalrequest import getRequest
from zope.interface import provider


logger = getLogger(__name__)

ANNOTATIONS_KEY = __name__


HAS_ELAN = True
try:
    from docpool.elan.behaviors.elandocument import IELANDocument
    from docpool.elan.config import ELAN_APP
    from docpool.elan.content.transfers import ensureScenariosInTarget
    from docpool.elan.content.transfers import knowsScen
except BaseException:
    HAS_ELAN = False


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
        description=_(
            "description_dpdocument_transferlog",
            default="Only used for archived documents.",
        ),
        required=False,
    )
    directives.omitted("transferLog")
    read_permission(transferLog="docpool.transfers.AccessTransfers")
    write_permission(transferLog="docpool.transfers.AccessTransfers")


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
        return getattr(self.context, "transferred", None)

    def _set_transferred(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.transferred = value

    transferred = property(_get_transferred, _set_transferred)

    @property
    def transferLog(self):
        return self.context.transferLog

    @transferLog.setter
    def transferLog(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.transferLog = value

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
            logRaw = logRaw and logRaw.replace("datetime.datetime", "datetime") or ""
            return eval(logRaw)

        else:
            if self.transferred:
                type_ = "receive"
                events = reversed(self.receiver_log)
            else:
                type_ = "send"
                events = reversed(self.sender_log)
                return [
                    {
                        "type": type_,
                        "by": event["user"],
                        "esd": event["esd_title"],
                        "timeraw": event["timestamp"],
                        "time": self.context.toLocalizedTime(
                            DateTime(event["timestamp"]), long_format=1
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
        if self.transferred or IArchiving(self.context).is_archive:
            return False
        if api.content.get_state(obj=self.context, default=None) != "published":
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

    def transferToTargets(self, targets=[]):
        """
        1) Determine all transfer folder objects.
        2) Put a copy of me in each of them, preserving timestamps.
        3) Add transfer information the copies.
        4) Add entries to sender logs.
        5) Make sure document types and scenarios exist in the target ESDs.
        6) Set workflow state of the copies according to folder permissions.
        7) Add entries to receiver logs.
        """

        def error_message(esd_to_title, msg):
            prefix = _("No transfer to")
            portalMessage(self.context, f"{prefix} {esd_to_title}. {msg}", type="error")

        def doIt():
            timestamp = datetime.now()
            userinfo_string = self.context._getUserInfoString(plain=True)
            dto = self.context.docTypeObj()
            if HAS_ELAN:
                elanobj = IELANDocument(self.context)

            for target in targets:
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
                        continue

                # b) Is my Scenario known, are unknown Scenarios accepted?
                scen_ok = transfer_folder.unknownScenDefault != "block"
                if not scen_ok and HAS_ELAN:
                    # check my precise Scenario
                    # FIXME: ELAN dependency
                    # TODO The following is inefficient in that it creates a list of
                    # full objects, but it effectively filters elanobj.scenarios for
                    # those that actually exist in the catalog. Is this necessary?
                    scens = elanobj.myScenarioObjects()
                    if scens:
                        scen_id = scens[0].getId()
                        if not knowsScen(transfer_folder, scen_id):
                            error_message(
                                esd_to_title,
                                _("Unknown scenario not accepted."),
                            )
                            continue
                    else:
                        error_message(esd_to_title, _("Document has no scenario."))
                        continue

                # At this point, transfer is allowed.
                logger.info(
                    "Transfer {} to {}.".format(
                        "/".join(self.context.getPhysicalPath()),
                        esd_to_title,
                    )
                )

                # 2) Put a copy of me in transfer folder, preserving timestamps.
                new_id = _copyPaste(self.context, transfer_folder)
                my_copy = transfer_folder._getOb(new_id)
                behaviors = set(ILocalBehaviorSupport(self.context).local_behaviors)
                if HAS_ELAN:
                    behaviors.add(ELAN_APP)  # FIXME: ELAN dependency
                ILocalBehaviorSupport(my_copy).local_behaviors = list(behaviors)

                # 3) Add transfer information to the copies.
                my_copy.transferred = timestamp
                my_copy.transferred_by = userinfo_string

                # 4) Add entry to sender log.
                scenario_ids = ", ".join(elanobj.scenarios or ()) if HAS_ELAN else ""
                self.sender_log += (
                    dict(
                        timestamp=timestamp,
                        user=userinfo_string,
                        scenario_ids=scenario_ids,
                        esd_title=esd_to_title,
                        transferfolder_uid=transfer_folder.UID(),
                    ),
                )

                # 5) Make sure document type and scenarios exist in the target ESD and
                #    are in a suitable state.
                ensureDocTypeInTarget(self.context, my_copy)

                if HAS_ELAN:
                    ensureScenariosInTarget(self.context, my_copy)

                # 6) Set workflow state of the copy according to folder permissions.
                ITransferable(my_copy).ensureState()
                my_copy.reindexObject()

                # 7) Add entry to receiver log.
                elancopy = IELANDocument(my_copy)
                scenario_ids = ", ".join(elancopy.scenarios or ()) if HAS_ELAN else ""
                self.receiver_log += (
                    dict(
                        timestamp=timestamp,
                        user=userinfo_string,
                        scenario_ids=scenario_ids,
                        esd_title=transfer_folder.getSendingESD().Title(),
                    ),
                )

                msg = _(
                    "Transferred to ${target_title}",
                    mapping={"target_title": esd_to_title},
                )
                api.portal.show_message(msg, self.request)

        execute_under_special_role(self.context, "Manager", doIt)

    def ensureState(self):
        """Put a transferred object in a state corresponding to the doctype permission.

        If there is no restriction on the transfer folder (permission is 'publish'),
        make sure workflow state of the copy is private if permission is 'needs
        confirmation' but public if it is 'publish'.

        """
        if self.transferred:
            tf = self.context.myDPTransferFolder()
            dtObj = self.context.docTypeObj()
            tstate = api.content.get_state(obj=dtObj)
            if tstate == "published":  # we do this for valid types only
                # determine the applicable permission
                perm = tf.doctypePermissions.get(dtObj.getId())
                dstate = api.content.get_state(self.context)
                if dstate == "private" and perm == "publish":
                    api.content.transition(self.context, "publish")
                if dstate == "published" and perm == "confirm":
                    api.content.transition(self.context, "retract")
            if HAS_ELAN:
                uscn = IELANDocument(self.context).unknownScenario()
                if uscn:
                    # Documents with unknown scenarios must be private
                    try:
                        api.content.transition(self.context, "retract")
                    except BaseException:
                        pass


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
                "/".join(obj.getPhysicalPath()),
            )
        )
        try:
            return tObj.transferToAll()
        except BaseException:
            pass
