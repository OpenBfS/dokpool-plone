from AccessControl import ClassSecurityInfo
from docpool.base.content.contentbase import ContentBase
from docpool.base.content.contentbase import IContentBase
from docpool.base.content.places import IPlaces
from docpool.base.marker import IImportingMarker
from docpool.elan import DocpoolMessageFactory as _
from docpool.elan.config import ELAN_APP
from logging import getLogger
from OFS.interfaces import IObjectWillBeRemovedEvent
from persistent.list import PersistentList
from plone import api
from plone.autoform import directives
from plone.base.i18nl10n import utranslate
from plone.base.interfaces.siteroot import IPloneSiteRoot
from plone.base.utils import safe_text
from plone.dexterity.content import Container
from Products.CMFCore.utils import getToolByName
from pygeoif import from_wkt
from z3c.form.browser.radio import RadioFieldWidget
from z3c.form.interfaces import IEditForm
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.interface import Invalid
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.lifecycleevent.interfaces import IObjectRemovedEvent

import datetime
import json


ARCHIVING_KEY = "docpool.elan.archiving"
logger = getLogger(__name__)


def initializeTimeOfEvent():
    return datetime.datetime.today()


def is_coordinate(value):
    if value:
        try:
            wkt = from_wkt(value)
        except Exception as exc:
            raise Invalid("Value is no a valid WKT.") from exc
        if not wkt.geom_type == "Point":
            raise Invalid("Value is not a Point.")
    return True


def is_point_or_polygon(value):
    if value:
        try:
            wkt = from_wkt(value)
        except Exception as exc:
            raise Invalid("Value is not a valid WKT.") from exc
        if wkt.geom_type not in ["Point", "Polygon"]:
            raise Invalid("Value is neither Point nor Polygon.")
    return True


class IDPEvent(IContentBase):
    """ """

    directives.widget(EventType=RadioFieldWidget)
    EventType = schema.Choice(
        title=_("label_dpevent_type", default="Type of event"),
        description=_("description_dpevent_type", default=""),
        required=True,
        source="docpool.elan.vocabularies.EventTypes",
    )

    directives.write_permission(Status="docpool.elan.ManageDPEvents")
    directives.widget(Status=RadioFieldWidget)
    Status = schema.Choice(
        title=_("label_dpevent_status", default="Status of the event"),
        description=_("description_dpevent_status", default=""),
        required=True,
        default="active",
        source="docpool.elan.vocabularies.Status",
    )

    TimeOfEvent = schema.Datetime(
        title=_("label_dpevent_timeofevent", default="Time of event"),
        description=_("description_dpevent_timeofevent", default=""),
        required=True,
        defaultFactory=initializeTimeOfEvent,
    )

    directives.write_permission(EventLocation="docpool.elan.ManageDPEvents")
    EventLocation = schema.Text(
        title=_("Event location"),
        required=False,
    )

    directives.write_permission(EventCoordinates="docpool.elan.ManageDPEvents")
    EventCoordinates = schema.Text(
        title=_("Event coordinates"),
        description=_("Example: POINT(12.293121814727781 48.60338936478996)"),
        required=False,
        constraint=is_coordinate,
    )

    directives.write_permission(AreaOfInterest="docpool.elan.ManageDPEvents")
    AreaOfInterest = schema.Text(
        title=_("Area of interest"),
        description=_(
            "Example: POLYGON((12.307090759277342 48.613051327205255,12.25421905517578 48.61339180317094,12.253875732421873 48.59216441224561,12.305803298950195 48.59182379315598,12.307090759277342 48.613051327205255))"
        ),
        required=False,
        constraint=is_point_or_polygon,
    )

    directives.widget(OperationMode=RadioFieldWidget)
    OperationMode = schema.Choice(
        title=_("Operation mode"),
        vocabulary="docpool.elan.vocabularies.Modes",
        required=True,
    )

    directives.widget(AlertingStatus=RadioFieldWidget)
    AlertingStatus = schema.Choice(
        title=_("label_dpevent_alerting_status", default="Status of Alerting"),
        description=_("description_dpevent_alerting_status", default=""),
        required=True,
        source="docpool.elan.vocabularies.AlertingStatus",
    )

    AlertingNote = schema.Text(
        title=_("label_dpevent_alteringnote", default="Alert Note"),
        description=_(
            "description_dpevent_alert_note",
            default='Content of message to IMIS-Users. This text is being displayed and can be overwritten. Status of Alerting has to be "initialized" to send it.',
        ),
        required=False,
    )

    SectorizingNetworks = schema.List(
        title=_("Sectorizing networks"),
        required=False,
        value_type=schema.Choice(source="docpool.elan.vocabularies.Networks"),
    )

    directives.omitted(IEditForm, "Journals")
    Journals = schema.List(
        title=_("Journals"),
        required=False,
        default=[
            "Einsatztagebuch BfS",
            "Einsatztagebuch RLZ",
            "Einsatztagebuch SSK",
            "Einsatztagebuch Messdienste",
        ],
        value_type=schema.TextLine(),
    )

    changelog = schema.Text(
        title=_("label_dpevent_changelog", default="Changelog"),
        description=_("Changelog"),
        required=False,
        readonly=True,
    )


@implementer(IDPEvent)
class DPEvent(Container, ContentBase):
    """ """

    APP = ELAN_APP

    security = ClassSecurityInfo()

    def dp_type(self):
        """
        We reuse the dp_type index for the scenario status.
        """
        return self.Status

    def archiveConfirmMsg(self):
        """
        Do you really want to archive this scenario?
        """
        return utranslate("docpool.elan", "archive_confirm_msg", context=self)

    def snapshot_confirm_msg(self):
        """
        Do you really want to create a snapshot of this event?
        The event stays active but all documents are moved to a archive.
        """
        return utranslate("docpool.elan", "snapshot_confirm_msg", context=self)

    def get_archiving_info(self):
        return IAnnotations(self).get(ARCHIVING_KEY, [])

    def set_archiving_info(self, info):
        annotations = IAnnotations(self)
        if ARCHIVING_KEY not in annotations:
            annotations[ARCHIVING_KEY] = PersistentList()
        annotations[ARCHIVING_KEY].append(info)

    def purge_archiving_info(self):
        IAnnotations(self).pop(ARCHIVING_KEY, None)
        self._p_changed = True

    @property
    def is_archive_uptodate(self):
        return not self.get_documents()

    def get_documents(self):
        """
        Collects all DPDocuments for the current scenario
        :return: list of brains
        """
        return api.content.find(
            portal_type="DPDocument",
            scenario=self.UID(),
            sort_on="sortable_title",
            context=IPlaces(self).content,
        )

    def canBeAssigned(self):
        """
        Can this scenario be assigned to documents?
        Is it published? Is it active?
        """
        wftool = getToolByName(self, "portal_workflow")
        return wftool.getInfoFor(self, "review_state") == "published" and self.Status == "active"

    def bounds(self, fieldname="AreaOfInterest"):
        coordinates = self.coordinates(fieldname)
        if not coordinates:
            return
        return coordinates.bounds

    def coordinates(self, fieldname="EventCoordinates"):
        wkt = getattr(self, fieldname, None)
        if not wkt:
            return
        return from_wkt(wkt)

    def event_type_title(self):
        vocab = api.portal.get_vocabulary("docpool.elan.vocabularies.EventTypes", context=self)
        return safe_text(vocab.getTerm(self.EventType).title)

    def operation_mode_title(self):
        if self.OperationMode is None:
            return None
        vocab = api.portal.get_vocabulary("docpool.elan.vocabularies.Modes")
        return safe_text(vocab.getTerm(self.OperationMode).title)

    def status_title(self):
        vocab = api.portal.get_vocabulary("docpool.elan.vocabularies.Status", context=self)
        return safe_text(vocab.getTerm(self.Status).title)

    def subscribed_docpools(self):
        return [
            dp
            for brain in api.content.find(portal_type="DocumentPool")
            if (dpevents := (dp := brain.getObject()).get("contentconfig", {}).get("scen")) is not None
            and self.UID() in dpevents.subscribed_events
        ]


def addLogEntry(obj):
    changelog = json.loads(obj.changelog or "[]")

    modes = obj.operation_mode_title()
    alerting_status = obj.AlertingStatus
    if alerting_status is not None:
        alerting_status_vocabulary = api.portal.get_vocabulary("docpool.elan.vocabularies.AlertingStatus")
        alerting_status = safe_text(alerting_status_vocabulary.getTerm(obj.AlertingStatus).title)
    entry = {}
    entry["Date"] = api.portal.get_localized_time(datetime.datetime.now(), long_format=1)
    entry["User"] = obj.formatUserInfo(obj._getUserInfoString())
    entry["Status"] = obj.Status
    entry["EventType"] = obj.EventType
    entry["Operation mode"] = modes
    entry["Alerting status"] = alerting_status
    entry["Alerting note"] = obj.AlertingNote
    entry["Sectorizing networks"] = ", ".join(obj.SectorizingNetworks or " ")
    # Check if there are changes to prevent duplicate log entries.
    if changelog and entry == changelog[-1]:
        return
    changelog.append(entry)
    obj.changelog = json.dumps(changelog)


@adapter(IDPEvent, IObjectModifiedEvent)
def eventChanged(obj, event=None):
    """ """
    if IImportingMarker.providedBy(getRequest()):
        return
    addLogEntry(obj)


@adapter(IDPEvent, IObjectWillBeRemovedEvent)
def check_delete_event(obj, event):
    if IPloneSiteRoot.providedBy(event.object):
        return
    if obj.subscribed_docpools():
        raise RuntimeError("Event cannot be deleted, still in use.")


@adapter(IDPEvent, IObjectRemovedEvent)
def eventRemoved(obj, event=None):
    """
    Make sure the routinemode event cannot be removed unless the whole docpool
    or the whole Plonesite is being deleted.
    """
    if getattr(obj, "__ALLOW_DELETE_DURING_UPGRADE_STEP__", False):
        return
    if IPloneSiteRoot.providedBy(event.object):
        return
    if obj.id == "routinemode":
        raise RuntimeError('The "routinemode" event cannot be removed.')
