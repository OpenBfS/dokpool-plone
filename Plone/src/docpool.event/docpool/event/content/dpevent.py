#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ""
__docformat__ = "plaintext"

import datetime
import json
from logging import getLogger

import plone.api as api
from AccessControl import ClassSecurityInfo
from Acquisition import aq_base
from DateTime import DateTime
from docpool.base.content.contentbase import ContentBase, IContentBase
from docpool.base.content.documentpool import IDocumentPool
from docpool.base.utils import portalMessage
from docpool.config.local.base import navSettings
from docpool.config.local.elan import ARCHIVESTRUCTURE
from docpool.config.local.transfers import TRANSFER_AREA
from docpool.config.utils import createPloneObjects, ploneId
from docpool.event import DocpoolMessageFactory as _
from docpool.event.utils import get_global_scenario_selection
from docpool.localbehavior.localbehavior import ILocalBehaviorSupport
from docpool.transfers.config import TRANSFERS_APP
from plone.autoform import directives
from plone.base.i18nl10n import utranslate
from plone.base.interfaces.siteroot import IPloneSiteRoot
from plone.base.utils import safe_text
from plone.dexterity.content import Container
from plone.protect.interfaces import IDisableCSRFProtection
from plone.supermodel import model
from Products.CMFCore.interfaces import IActionSucceededEvent
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import log, log_exc, parent
from pygeoif import geometry
from z3c.form.browser.radio import RadioFieldWidget
from z3c.form.interfaces import IEditForm
from z3c.relationfield.schema import RelationChoice, RelationList
from zope import schema
from zope.component import adapter, getUtility
from zope.interface import Interface, Invalid, alsoProvides, implementer
from zope.lifecycleevent.interfaces import (
    IObjectAddedEvent,
    IObjectModifiedEvent,
    IObjectRemovedEvent,
)

logger = getLogger("dpevent")


def initializeTimeOfEvent():
    return datetime.datetime.today()


def is_coordinate(value):
    if value:
        try:
            wkt = geometry.from_wkt(value)
        except Exception:
            raise Invalid("Value is no a valid WKT.")
        if not wkt.geom_type == "Point":
            raise Invalid("Value is not a Point.")
    return True


def is_polygon(value):
    if value:
        try:
            wkt = geometry.from_wkt(value)
        except Exception:
            raise Invalid("Value is not a valid WKT.")
        if not wkt.geom_type == "Polygon":
            raise Invalid("Value is not a Polygon.")
        raise Invalid("Vaueis not a valid coordinate.")
    return True


class IDPEvent(model.Schema, IContentBase):
    """ """

    directives.write_permission(Substitute="docpool.event.ManageDPEvents")
    directives.widget(Substitute="z3c.form.browser.select.SelectFieldWidget")
    Substitute = RelationChoice(
        title=_("label_dpevent_substitute", default="Substitute event"),
        description=_(
            "description_dpevent_substitute",
            default="Only relevant for private events received from another organisation. Allows you map content for this event to one of your own events.",  # noqa: E501
        ),
        required=False,
        source="docpool.event.vocabularies.EventSubstitutes",
    )

    directives.widget(EventType=RadioFieldWidget)
    EventType = schema.Choice(
        title=_("label_dpevent_type", default="Type of event"),
        description=_("description_dpevent_type", default=""),
        required=True,
        source="docpool.event.vocabularies.EventTypes",
    )

    directives.write_permission(Status="docpool.event.ManageDPEvents")
    directives.widget(Status=RadioFieldWidget)
    Status = schema.Choice(
        title=_("label_dpevent_status", default="Status of the event"),
        description=_("description_dpevent_status", default=""),
        required=True,
        default="active",
        source="docpool.event.vocabularies.Status",
    )

    TimeOfEvent = schema.Datetime(
        title=_("label_dpevent_timeofevent", default="Time of event"),
        description=_("description_dpevent_timeofevent", default=""),
        required=True,
        defaultFactory=initializeTimeOfEvent,
    )

    # directives.widget(EventPhase=AutocompleteFieldWidget)
    directives.widget(EventPhase="z3c.form.browser.select.SelectFieldWidget")
    EventPhase = RelationChoice(
        title=_("Scenario & Phase"),
        vocabulary="docpool.event.vocabularies.Phases",
        required=False,
    )

    directives.write_permission(EventLocation="docpool.event.ManageDPEvents")
    directives.widget(EventLocation="z3c.form.browser.select.SelectFieldWidget")
    EventLocation = RelationChoice(
        title=_("Event location"),
        vocabulary="docpool.event.vocabularies.PowerStations",
        required=False,
    )

    directives.write_permission(EventCoordinates="docpool.event.ManageDPEvents")
    EventCoordinates = schema.Text(
        title=_("Event coordinates"),
        description=_("Example: POINT(12.293121814727781 48.60338936478996)"),
        required=False,
        constraint=is_coordinate,
    )

    directives.write_permission(AreaOfInterest="docpool.event.ManageDPEvents")
    AreaOfInterest = schema.Text(
        title=_("Area of interest"),
        description=_(
            "Example: POLYGON((12.307090759277342 48.613051327205255,12.25421905517578 48.61339180317094,12.253875732421873 48.59216441224561,12.305803298950195 48.59182379315598,12.307090759277342 48.613051327205255))"
        ),
        required=False,
        constraint=is_polygon,
    )

    directives.widget(OperationMode=RadioFieldWidget)
    OperationMode = schema.Choice(
        title=_("Operation mode"),
        vocabulary="docpool.event.vocabularies.Modes",
        required=True,
    )

    directives.widget(AlertingStatus=RadioFieldWidget)
    AlertingStatus = schema.Choice(
        title=_("label_dpevent_alerting_status", default="Status of Alerting"),
        description=_("description_dpevent_alerting_status", default=""),
        required=True,
        source="docpool.event.vocabularies.AlertingStatus",
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
        value_type=schema.Choice(source="docpool.event.vocabularies.SampleType"),
    )

    directives.widget(
        SectorizingNetworks="z3c.form.browser.select.CollectionSelectFieldWidget"
    )
    SectorizingNetworks = RelationList(
        title=_("Sectorizing networks"),
        required=False,
        value_type=RelationChoice(source="docpool.event.vocabularies.Networks"),
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

    security = ClassSecurityInfo()

    def print_dict(self):
        """

        :return:
        """
        return self.__dict__

    def migrate(self):
        request = self.REQUEST
        alsoProvides(request, IDisableCSRFProtection)
        f = parent(self)
        if hasattr(self, "_setPortalTypeName"):
            self._setPortalTypeName("DPEvent")
        myid = self.getId()
        del f[myid]
        self.__class__ = DPEvent
        f[myid] = self
        logger.info(self.__class__)
        logger.info(self.getPortalTypeName())

    def migrateProperties(self):
        request = self.REQUEST
        alsoProvides(request, IDisableCSRFProtection)

        self = aq_base(self)
        if hasattr(self, "status"):
            self.Status = self.status
        if hasattr(self, "exercise"):
            self.Exercise = self.exercise
        if hasattr(self, "timeOfEvent"):
            self.TimeOfEvent = self.timeOfEvent
        if hasattr(self, "substitute"):
            self.Substitute = self.substitute

    def phaseInfo(self):
        """
        :return:
        """
        if self.EventPhase:
            return self.EventPhase.to_object.getPhaseTitle()
        return ""

    def dp_type(self):
        """
        We reuse the dp_type index for the scenario status.
        """
        return self.Status

    def purgeConfirmMsg(self):
        """
        Do you really want to remove all documents from this scenario?
        """
        return utranslate("docpool.event", "purge_confirm_msg", context=self)

    def archiveConfirmMsg(self):
        """
        Do you really want to archive this scenario?
        """
        return utranslate("docpool.event", "archive_confirm_msg", context=self)

    security.declareProtected("Modify portal content", "archiveAndClose")

    def archiveAndClose(self, REQUEST):
        """
        Saves all content for this scenario to an archive, deletes the original content,
        and sets the scenario to state "closed".
        """
        alsoProvides(REQUEST, IDisableCSRFProtection)
        global_scenarios = get_global_scenario_selection()
        global_scenarios[self.getId()] = "closed"
        archive = self._createArchive()
        contentarea = self.content
        contentarea_path = "/".join(contentarea.getPhysicalPath())

        archive_contentarea = archive.content
        mdocs = self._getDocumentsForScenario(path=contentarea_path)
        for doc in mdocs:
            target_folder = self._ensureTargetFolder(doc, archive_contentarea)
            self._copyDocument(target_folder, doc)

        self.purge()
        self.Status = "closed"
        # Move DPEvent into archive and redirect to it
        archived_event = api.content.move(self, target=archive)
        archived_event.reindexObject()
        api.portal.show_message(_("Scenario archived"), REQUEST)
        return REQUEST.response.redirect(archived_event.absolute_url())

    def _ensureTargetFolder(self, doc, aroot):
        """
        Make sure that a personal or group folder with proper permissions
        exists for this document in the archive.
        """
        # 1. check whether this is a personal or a group document
        path = doc.getPath().split("/")
        isGroup = "Groups" in path
        if isGroup:
            aroot = aroot.Groups
        isTransfer = "Transfers" in path
        if isTransfer:
            aroot = aroot.Transfers
        isMember = "Members" in path
        if isMember:
            aroot = aroot.Members
        # 2. check for which user / group
        if len(path) >= 4:
            if isGroup or isTransfer or isMember:
                fname = path[5]
            else:
                fname = path[4]
        # 3. check for corresponding folder
        hasFolder = aroot.hasObject(fname)
        # 4. if it doesn't exist: create it
        if not hasFolder:
            if isGroup:
                folderType = "GroupFolder"
            if isMember:
                folderType = "UserFolder"
            if isTransfer:
                folderType = "DPTransferFolder"
            # if not we create a new folder
            aroot.invokeFactory(folderType, id=fname)
        af = aroot._getOb(fname)
        # 5. and copy the local roles
        mroot = self.content.Members
        if isGroup:
            mroot = self.content.Groups
        if isTransfer:
            mroot = self.content.Transfers
        mf = mroot._getOb(fname)
        af.setTitle(mf.Title())
        if not isTransfer:
            mtool = getToolByName(self, "portal_membership")
            mtool.setLocalRoles(af, [fname], "Owner")
        af.reindexObject()
        af.reindexObjectSecurity()
        return af

    def _copyDocument(self, target_folder_obj, source_brain):
        """
        Copy utility
        """
        # TODO: transferLog fuellen und DB Eintraege loeschen
        # print source_brain.getId
        source_obj = source_brain.getObject()
        # determine parent folder for copy
        p = parent(source_obj)
        # if source_obj.getId() == 'ifinprojection.2012-08-08.4378013443':
        #    p._delOb('ifinprojection.2012-08-08.4378013443')
        #    return
        cb_copy_data = p.manage_copyObjects(source_obj.getId())
        result = target_folder_obj.manage_pasteObjects(cb_copy_data)
        # Now do some repairs
        if len(result) == 1:
            new_id = result[0]["new_id"]
            copied_obj = target_folder_obj._getOb(new_id)
            mdate = source_obj.modified()
            copied_obj.scenarios = []
            wf_state = source_brain.review_state
            wftool = getToolByName(self, "portal_workflow")
            # print wf_state, wftool.getInfoFor(copied_obj, 'review_state')
            if (
                wf_state == "published"
                and wftool.getInfoFor(copied_obj, "review_state") != "published"
            ):
                wftool.doActionFor(copied_obj, "publish")
            if (
                wf_state == "pending"
                and wftool.getInfoFor(copied_obj, "review_state") == "private"
            ):
                wftool.doActionFor(copied_obj, "submit")
            copied_obj.setModificationDate(mdate)
            events = source_obj.doc_extension(TRANSFERS_APP).transferEvents()
            copied_obj.transferLog = str(events)
            copied_obj.reindexObject()
            copied_obj.reindexObjectSecurity()
        else:
            log("Could not archive %s" % source_obj.absolute_url())

    def _getDocumentsForScenario(self, **kwargs):
        """
        Collects all DPDocuments for the current scenario
        :return: list of brains
        """
        #        args = {'object_provides':IDPDocument.__identifier__, 'scenarios': self.getId()}
        args = {"portal_type": "DPDocument", "scenarios": self.getId()}
        args.update(kwargs)
        cat = getToolByName(self, "portal_catalog")
        return cat(args)

    def _createArchive(self):
        """
        We create an archive object. Into it, we copy the complete ESD hierarchy.
        We also create two folders "Members" and "Groups", which will hold all the
        documents for the scenario.
        """
        a = self.archive  # Acquire root for archives
        e = self.esd  # Acquire esd root
        now = safe_text(self.toLocalizedTime(DateTime(), long_format=1))
        id = ploneId(self, f"{self.getId()}_{now}")
        title = f"{safe_text(self.Title())} {now}"
        # create the archive root
        a.invokeFactory(id=id, type_name="ELANArchive", title=title)
        arc = a._getOb(id)  # get new empty archive
        arc.setDescription(self.Description())
        # create the document folders
        createPloneObjects(arc, ARCHIVESTRUCTURE)
        createPloneObjects(arc.content, TRANSFER_AREA)

        navSettings(arc)

        # copy the ESD folders
        objs = [
            o.getId
            for o in e.getFolderContents(
                {"portal_type": ["ELANSection", "ELANDocCollection"]}
            )
        ]
        # print objs
        cb_copy_data = e.manage_copyObjects(objs)  # Copy aus der Quelle
        result = arc.esd.manage_pasteObjects(cb_copy_data)
        arc.esd.setDefaultPage("overview")

        return arc

    security.declareProtected("Modify portal content", "purge")

    def purge(self, REQUEST=None):
        """
        Deletes the content for this scenario but leaves the status unchanged.
        Documents are deleted if they are not part of any other scenario.
        If they are part of another scenario, only the tag for the current scenario is removed.
        """
        alsoProvides(REQUEST or self.REQUEST, IDisableCSRFProtection)
        # TODO im EVENT auf Elandoc DB-Eintraege loeschen.
        m = self.content.Members
        mpath = "/".join(m.getPhysicalPath())
        # We now query the catalog for all documents belonging to this scenario within
        # the personal and group folders
        mdocs = self._getDocumentsForScenario(path=mpath)
        for doc in mdocs:
            self._purgeDocument(doc)
        g = self.content.Groups
        gpath = "/".join(g.getPhysicalPath())
        # We now query the catalog for all documents belonging to this scenario within
        # the personal and group folders
        gdocs = self._getDocumentsForScenario(path=gpath)
        for doc in gdocs:
            self._purgeDocument(doc)
        t = self.content.Transfers
        tpath = "/".join(t.getPhysicalPath())
        # We now query the catalog for all documents belonging to this scenario within
        # the personal and group folders
        tdocs = self._getDocumentsForScenario(path=tpath)
        for doc in tdocs:
            self._purgeDocument(doc)
        if REQUEST:
            portalMessage(
                self, _("There are no more documents for this scenario."), "info"
            )
            return self.restrictedTraverse("view")()

    def _purgeDocument(self, source_brain):
        """
        Delete utility
        """
        from docpool.elan.behaviors.elandocument import IELANDocument
        from docpool.elan.config import ELAN_APP

        source_obj = source_brain.getObject()
        # determine parent folder for copy
        scns = None
        try:
            scns = IELANDocument(source_obj).scenarios
        except BaseException:
            # Object could have lost its ELAN behavior but that means we can
            # potentially delete it
            scns = ["dummy"]
        if len(scns) == 1:  # only the one scenario --> potential delete
            # Check for other applications than ELAN
            apps = ILocalBehaviorSupport(source_obj).local_behaviors
            if apps and len(apps) > 1:  # There are others --> only remove ELAN behavior
                try:
                    apps.remove(ELAN_APP)
                    ILocalBehaviorSupport(source_obj).local_behaviors = list(set(apps))
                except Exception as e:
                    log_exc(e)
            else:  # we delete
                p = parent(source_obj)
                p.manage_delObjects([source_obj.getId()])
        else:  # Only remove the scenario
            scns = list(scns)
            scns.remove(self.getId())
            source_obj.scenarios = scns
            source_obj.reindexObject()

    def selectGlobally(self):
        global_scenarios = get_global_scenario_selection()
        global_scenarios[self.getId()] = "selected"

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
                pass
            journal = api.content.create(
                container=self,
                type="Journal",
                title=title,
                id=journal_id,
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
        return geometry.from_wkt(wkt)

    def event_type_title(self):
        vocab = getUtility(Interface, name="docpool.event.vocabularies.EventTypes")
        return vocab(self).getTerm(self.EventType).title


class ELANScenario(DPEvent):
    pass


@adapter(IDPEvent, IObjectAddedEvent)
def eventAdded(obj, event=None):
    """
    For new scenarios, add them to each user's personal selection and
    create the journals.
    """
    # print "scenarioAdded"
    obj.selectGlobally()
    obj.createDefaultJournals()


def addLogEntry(obj):
    changelog = json.loads(obj.changelog or "[]")
    entry = {}
    entry["Date"] = api.portal.get_localized_time(
        datetime.datetime.now(), long_format=1
    )
    entry["User"] = obj._getUserInfoString()
    entry["Status"] = obj.Status
    entry["EventType"] = obj.EventType
    entry["Operation mode"] = obj.OperationMode
    entry["Alerting status"] = obj.AlertingStatus
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
    global_scenarios[obj.getId()] = "removed"


@adapter(IDPEvent, IActionSucceededEvent)
def eventPublished(obj, event=None):
    if event.__dict__["action"] == "publish":
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
                if scens and obj.getId() in scens:
                    docobj.reindexObject()
                    # print "changed", docobj
            except Exception as e:
                log_exc(e)
