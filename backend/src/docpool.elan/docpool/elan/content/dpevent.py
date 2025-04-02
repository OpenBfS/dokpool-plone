from AccessControl import ClassSecurityInfo
from docpool.base.content.archiving import IArchiving
from docpool.base.content.contentbase import ContentBase
from docpool.base.content.contentbase import IContentBase
from docpool.base.content.documentpool import IDocumentPool
from docpool.base.marker import IImportingMarker
from docpool.elan import DocpoolMessageFactory as _
from docpool.elan.config import ELAN_APP
from docpool.elan.utils import get_global_scenario_selection
from logging import getLogger
from plone import api
from plone.autoform import directives
from plone.base.i18nl10n import utranslate
from plone.base.interfaces.siteroot import IPloneSiteRoot
from plone.base.utils import safe_text
from plone.dexterity.content import Container
from Products.CMFCore.interfaces import IActionSucceededEvent
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import log
from Products.CMFPlone.utils import log_exc
from pygeoif import from_wkt
from z3c.form.browser.radio import RadioFieldWidget
from z3c.form.interfaces import IEditForm
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.component import getUtility
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import Invalid
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.lifecycleevent.interfaces import IObjectRemovedEvent
from zope.schema.interfaces import IVocabularyFactory

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
        except Exception:
            raise Invalid("Value is no a valid WKT.")
        if not wkt.geom_type == "Point":
            raise Invalid("Value is not a Point.")
    return True


def is_point_or_polygon(value):
    if value:
        try:
            wkt = from_wkt(value)
        except Exception:
            raise Invalid("Value is not a valid WKT.")
        if not wkt.geom_type in ["Point", "Polygon"]:
            raise Invalid("Value is neither Point nor Polygon.")
    return True


class IDPEvent(IContentBase):
    """ """

    directives.write_permission(Substitute="docpool.elan.ManageDPEvents")
    directives.widget(Substitute="plone.app.z3cform.widgets.select.SelectFieldWidget")
    Substitute = RelationChoice(
        title=_("label_dpevent_substitute", default="Substitute event"),
        description=_(
            "description_dpevent_substitute",
            default="Only relevant for private events received from another organisation. Allows you map content for this event to one of your own events.",  # noqa: E501
        ),
        required=False,
        source="docpool.elan.vocabularies.EventSubstitutes",
    )

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

    EventPhase = schema.TextLine(
        title=_("Scenario & Phase"),
        required=False,
    )

    directives.write_permission(EventLocation="docpool.elan.ManageDPEvents")
    directives.widget(
        EventLocation="plone.app.z3cform.widgets.select.SelectFieldWidget"
    )
    EventLocation = RelationChoice(
        title=_("Event location"),
        vocabulary="docpool.elan.vocabularies.PowerStations",
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
        ),  # noqa: E501
        required=False,
    )

    SectorizingSampleTypes = schema.List(
        title=_("Sectorizing sample types"),
        required=False,
        value_type=schema.Choice(source="docpool.elan.vocabularies.SampleType"),
    )

    directives.widget(
        SectorizingNetworks="z3c.form.browser.select.CollectionSelectFieldWidget"
    )
    SectorizingNetworks = RelationList(
        title=_("Sectorizing networks"),
        required=False,
        value_type=RelationChoice(source="docpool.elan.vocabularies.Networks"),
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

    def phaseInfo(self):
        """
        :return:
        """
        return self.EventPhase

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
        return IAnnotations(self).get(ARCHIVING_KEY, {})

    def set_archiving_info(self, info):
        IAnnotations(self)[ARCHIVING_KEY] = info

    def selectGlobally(self):
        global_scenarios = get_global_scenario_selection()
        global_scenarios[self.UID()] = "selected"

    def createDefaultJournals(self):
        """
        Creates journals inside the event
        :return:"""
        if not self.Journals:
            return
        docpool = self.myDocumentPool()
        prefix = docpool.prefix or docpool.getId()
        for index, title in enumerate(self.Journals, start=1):
            title = title.strip()
            # Skip empty lines
            if not title:
                continue
            journal_id = f"journal{str(index)}"
            # Skip if it already exists
            if self.get(journal_id):
                continue
            journal = api.content.create(
                container=self,
                type="Journal",
                title=title,
                id=journal_id,
                exclude_from_nav=False,
            )
            # Grant local role to Journal Editor Groups
            api.group.grant_roles(
                groupname=f"{prefix}_Journal{index}_Editors",
                roles=["JournalEditor"],
                obj=journal,
            )
            # Grant local role to Journal Reader Groups
            api.group.grant_roles(
                groupname=f"{prefix}_Journal{index}_Readers",
                roles=["JournalReader"],
                obj=journal,
            )

    def deleteEventReferences(self):
        """ """
        self.Substitute = None
        self.reindexObject()

    def canBeAssigned(self):
        """
        Can this scenario be assigned to documents?
        Is it published? Is it active?
        """
        wftool = getToolByName(self, "portal_workflow")
        return (
            wftool.getInfoFor(self, "review_state") == "published"
            and self.Status == "active"
        )

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
        vocab = getUtility(Interface, name="docpool.elan.vocabularies.EventTypes")
        return vocab(self).getTerm(self.EventType).title


@adapter(IDPEvent, IObjectAddedEvent)
def eventAdded(obj, event=None):
    """
    For new scenarios, add them to each user's personal selection and
    create the journals.
    """
    if IImportingMarker.providedBy(getRequest()):
        return
    if IArchiving(obj).is_archive:
        return
    obj.selectGlobally()
    obj.createDefaultJournals()


def addLogEntry(obj):
    changelog = json.loads(obj.changelog or "[]")

    modes = obj.OperationMode
    if modes is not None:
        modes_vocabulary = getUtility(
            IVocabularyFactory, "docpool.elan.vocabularies.Modes"
        )()
        modes = safe_text(modes_vocabulary.getTerm(obj.OperationMode).title)
    alerting_status = obj.AlertingStatus
    if alerting_status is not None:
        alerting_status_vocabulary = getUtility(
            IVocabularyFactory, "docpool.elan.vocabularies.AlertingStatus"
        )()
        alerting_status = safe_text(
            alerting_status_vocabulary.getTerm(obj.AlertingStatus).title
        )
    entry = {}
    entry["Date"] = api.portal.get_localized_time(
        datetime.datetime.now(), long_format=1
    )
    entry["User"] = obj._getUserInfoString()
    entry["Status"] = obj.Status
    entry["EventType"] = obj.EventType
    entry["Operation mode"] = modes
    entry["Alerting status"] = alerting_status
    entry["Alerting note"] = obj.AlertingNote
    entry["Phase"] = obj.phaseInfo()
    entry["Sectorizing sample types"] = ", ".join(
        obj.SectorizingSampleTypes if obj.SectorizingSampleTypes is not None else " "
    )
    entry["Sectorizing networks"] = ", ".join(
        (n.to_object.title for n in obj.SectorizingNetworks)
        if obj.SectorizingNetworks is not None
        else " "
    )
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

    if obj.Status != "active":
        obj.deleteEventReferences()
        # print obj.Substitute
        if obj.Substitute:
            sscen = obj.Substitute.to_object
            if not sscen.canBeAssigned():
                log("Substitute can not be assigned. Not published or not active.")
                return
            # Update all objects for this scenario
            m = obj.content
            mpath = "/".join(m.getPhysicalPath())
            # We now query the catalog for all documents belonging to this scenario within
            # the personal and group folders
            args = {"portal_type": "DPDocument", "path": mpath}
            cat = getToolByName(obj, "portal_catalog")
            mdocs = cat(args)
            for doc in mdocs:
                try:
                    docobj = doc.getObject()
                    scens = docobj.scenarios
                    # print docobj, scens
                    if scens and obj.getId() in scens:
                        scens.remove(obj.getId())
                        scens.append(sscen.getId())
                        docobj.scenarios = scens
                        docobj.reindexObject()
                        # print "changed", docobj
                except Exception as e:
                    log_exc(e)


@adapter(IDPEvent, IObjectRemovedEvent)
def eventRemoved(obj, event=None):
    """
    Make sure the routinemode event cannot be removed unless the whole docpool
    or the whole Plonesite is being deleted.
    """
    if IPloneSiteRoot.providedBy(event.object) or IDocumentPool.providedBy(
        event.object
    ):
        return
    if obj.id == "routinemode":
        raise RuntimeError('The "routinemode" event cannot be removed.')

    global_scenarios = get_global_scenario_selection()
    global_scenarios[obj.UID()] = "removed"


@adapter(IDPEvent, IActionSucceededEvent)
def eventPublished(obj, event=None):
    if event.__dict__["action"] == "publish":
        if IImportingMarker.providedBy(getRequest()):
            return
        # Update all objects for this scenario
        m = obj.content
        mpath = "/".join(m.getPhysicalPath())
        args = {"portal_type": "DPDocument", "path": mpath}
        cat = getToolByName(obj, "portal_catalog")
        mdocs = cat(args)
        for doc in mdocs:
            try:
                docobj = doc.getObject()
                scens = docobj.scenarios
                # print docobj, scens
                if scens and obj.UID() in scens:
                    docobj.reindexObject()
                    # print "changed", docobj
            except Exception as e:
                log_exc(e)
