# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

from __future__ import print_function
__author__ = ''
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Acquisition import aq_base
from collective.z3cform.mapwidget import WKT
from DateTime import DateTime
from docpool.base.content.contentbase import ContentBase
from docpool.base.content.contentbase import IContentBase
from docpool.base.content.documentpool import IDocumentPool
from docpool.config.local.base import navSettings
from docpool.config.local.elan import ARCHIVESTRUCTURE
from docpool.config.local.transfers import TRANSFER_AREA
from docpool.config.utils import createPloneObjects
from docpool.config.utils import ploneId
from docpool.elan.behaviors.elandocument import IELANDocument
from docpool.elan.config import ELAN_APP
from docpool.event import DocpoolMessageFactory as _
from docpool.event.utils import get_global_scenario_selection
from docpool.localbehavior.localbehavior import ILocalBehaviorSupport
from docpool.transfers.config import TRANSFERS_APP
from elan.journal.adapters import IJournalEntryContainer
from elan.journal.adapters import JournalEntry
from logging import getLogger
from plone import api
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.dexterity.utils import safe_unicode
from plone.protect.interfaces import IDisableCSRFProtection
from plone.supermodel import model
from Products.CMFCore.interfaces import IActionSucceededEvent
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.i18nl10n import utranslate
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from Products.CMFPlone.utils import log
from Products.CMFPlone.utils import log_exc
from Products.CMFPlone.utils import parent
from pygeoif import geometry
from z3c.form.browser.radio import RadioFieldWidget
from z3c.form.interfaces import IEditForm
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.component import adapter
from zope.component import getUtility
from zope.interface import Interface
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.lifecycleevent.interfaces import IObjectRemovedEvent

import datetime
import json
import transaction


logger = getLogger("dpevent")


def initializeTimeOfEvent():
    return datetime.datetime.today()


class IDPEvent(model.Schema, IContentBase):
    """
    """

    directives.write_permission(Substitute='docpool.event.ManageDPEvents')
    directives.widget(Substitute='z3c.form.browser.select.SelectFieldWidget')
    Substitute = RelationChoice(
        title=_(u'label_dpevent_substitute', default=u'Substitute event'),
        description=_(
            u'description_dpevent_substitute',
            default=u'Only relevant for private events received from another organisation. Allows you map content for this event to one of your own events.',  # noqa: E501
        ),
        required=False,
        source="docpool.event.vocabularies.EventSubstitutes",
    )

    directives.widget(EventType=RadioFieldWidget)
    EventType = schema.Choice(
        title=_(u'label_dpevent_type', default=u'Type of event'),
        description=_(u'description_dpevent_type', default=u''),
        required=True,
        source='docpool.event.vocabularies.EventTypes',
    )

    directives.write_permission(Status='docpool.event.ManageDPEvents')
    directives.widget(Status=RadioFieldWidget)
    Status = schema.Choice(
        title=_(u'label_dpevent_status', default=u'Status of the event'),
        description=_(u'description_dpevent_status', default=u''),
        required=True,
        default='active',
        source="docpool.event.vocabularies.Status",
    )

    TimeOfEvent = schema.Datetime(
        title=_(u'label_dpevent_timeofevent', default=u'Time of event'),
        description=_(u'description_dpevent_timeofevent', default=u''),
        required=True,
        defaultFactory=initializeTimeOfEvent,
    )

    # directives.widget(EventPhase=AutocompleteFieldWidget)
    directives.widget(
        EventPhase='z3c.form.browser.select.SelectFieldWidget')
    EventPhase = RelationChoice(
        title=_(u"Scenario & Phase"),
        vocabulary=u"docpool.event.vocabularies.Phases",
        required=False,
    )

    directives.write_permission(EventLocation='docpool.event.ManageDPEvents')
    directives.widget(
        EventLocation='z3c.form.browser.select.SelectFieldWidget')
    EventLocation = RelationChoice(
        title=_(u'Event location'),
        vocabulary=u"docpool.event.vocabularies.PowerStations",
        required=False,
    )

    directives.write_permission(EventCoordinates='docpool.event.ManageDPEvents')
    EventCoordinates = WKT(
        title=_(u"Event coordinates"),
        required=False,
    )

    directives.write_permission(AreaOfInterest='docpool.event.ManageDPEvents')
    AreaOfInterest = WKT(
        title=_(u"Area of interest"),
        required=False,
    )

    directives.widget(OperationMode=RadioFieldWidget)
    OperationMode = schema.Choice(
        title=_(u'Operation mode'),
        vocabulary=u"docpool.event.vocabularies.Modes",
        required=True,
    )

    directives.widget(AlertingStatus=RadioFieldWidget)
    AlertingStatus = schema.Choice(
        title=_(u'label_dpevent_alerting_status', default=u'Status of Alerting'),
        description=_(u'description_dpevent_alerting_status', default=u''),
        required=True,
        source="docpool.event.vocabularies.AlertingStatus",
    )

    AlertingNote = schema.Text(
        title=_(u'label_dpevent_alteringnote', default=u'Alert Note'),
        description=_(u'description_dpevent_alert_note', default=u'Content of message to IMIS-Users. This text is being displayed and can be overwritten. Status of Alerting has to be "initialized" to send it.'),  # noqa: E501
        required=False,
        )

    SectorizingSampleTypes = schema.List(
        title=_(u'Sectorizing sample types'),
        required=False,
        value_type=schema.Choice(
            source=u"docpool.event.vocabularies.SampleType"),
    )

    directives.widget(
        SectorizingNetworks='z3c.form.browser.select.CollectionSelectFieldWidget'
    )
    SectorizingNetworks = RelationList(
        title=_(u'Sectorizing networks'),
        required=False,
        value_type=RelationChoice(
            source=u'docpool.event.vocabularies.Networks'),
    )

    directives.omitted(IEditForm, 'Journals')
    Journals = schema.List(
        title=_(u'Journals'),
        required=False,
        default=[
            u'Einsatztagebuch BfS',
            u'Einsatztagebuch RLZ',
            u'Einsatztagebuch SSK',
            u'Einsatztagebuch Messdienste',
            ],
        value_type=schema.TextLine(),
    )

    changelog = schema.Text(
        title=_(u'label_dpevent_changelog', default=u'Changelog'),
        description=_(u'Changelog'),
        required=False,
        readonly=True,
    )


@implementer(IDPEvent)
class DPEvent(Container, ContentBase):
    """
    """

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
        if hasattr(self, '_setPortalTypeName'):
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

    def archiveConfirmMsg(self):
        """
        Do you really want to archive this scenario?
        """
        return utranslate("docpool.event", "archive_confirm_msg", context=self)

    def snapshot_confirm_msg(self):
        """
        Do you really want to create a snapshot of this event?
        The event stays active but all documents are moved to a archive.
        """
        return utranslate("docpool.event", "snapshot_confirm_msg", context=self)

    security.declareProtected("Modify portal content", "archiveAndClose")
    def archiveAndClose(self, REQUEST):
        """
        Saves all content for this scenario to an archive, deletes the original content,
        and sets the scenario to state "closed".

        This can take a long time since associated DPDocuments can have many attechments
        and all need to be copied or moved and reindexed. This is why we make savepoints.
        """
        alsoProvides(REQUEST, IDisableCSRFProtection)

        # 1. Disable scenario to prevent new data from being added for it
        global_scenarios = get_global_scenario_selection()
        global_scenarios[self.id] = 'closed'
        self.Status = 'closed'
        transaction.savepoint(optimistic=True)

        # 2. Create Archive
        archive = self._createArchive()
        archive_contentarea = archive.content
        logger.info(u"Archiving DPEvent %s to %s", self.title, archive.absolute_url())
        contentarea = self.content
        contentarea_path = "/".join(contentarea.getPhysicalPath())

        # 3. Move or Copy related DPDocuments
        brains = self._getDocumentsForScenario(path=contentarea_path)
        total = len(brains)
        logger.info(u"Archiving %s items associated with DPEvent %s. This may take a while...", total, self.absolute_url())
        for index, brain in enumerate(brains, start=1):
            obj = brain.getObject()
            target_folder = self._ensureTargetFolder(obj, archive_contentarea)
            if self.can_move(obj):
                self._move_to_archive(target_folder, obj)
            else:
                self._copy_to_archive(target_folder, obj)

            if not index % 10:
                logger.info(u"Archived %s of %s documents...", index, total)
                transaction.savepoint(optimistic=True)

        # 4. Move DPEvent into archive and redirect to it
        archived_event = api.content.move(self, target=archive)
        archived_event.reindexObject()
        # local roles were set when adding items to the archive but reindexing was deferred.
        archive_contentarea.reindexObjectSecurity()
        logger.info(u"Finished archiving DPEvent %s", archived_event.title)
        api.portal.show_message(_("Scenario archived"), REQUEST)
        return REQUEST.response.redirect(archived_event.absolute_url())

    security.declareProtected("Modify portal content", "snapshot")
    def snapshot(self, REQUEST=None):
        """
        Similar to archiveAndClose but leave the old event as is.
        Previously this was two seperate actions snapshot & purge. But if content would be
        added between snapshop and purge that would be lost forever.

        * Create Archive for event but leave Event unchanged
        * Copy Journals and Event to Archive
        * Purge Journals
        * Purge Event (move content to archive unless used by other apps or events)
        """
        alsoProvides(REQUEST, IDisableCSRFProtection)

        # 1. Create Archive
        archive = self._createArchive()
        archive_contentarea = archive.content
        logger.info(u"Create snapshot of DPEvent %s in %s", self.title, archive.absolute_url())

        # 2. Move or Copy related DPDocuments (previously done by purge)
        contentarea = self.content
        contentarea_path = "/".join(contentarea.getPhysicalPath())
        brains = self._getDocumentsForScenario(path=contentarea_path)
        total = len(brains)
        logger.info(u"Archiving %s items associated with DPEvent %s. This may take a while...", total, self.absolute_url())
        for index, brain in enumerate(brains, start=1):
            obj = brain.getObject()
            target_folder = self._ensureTargetFolder(obj, archive_contentarea)
            if self.can_move(obj):
                self._move_to_archive(target_folder, obj)
            else:
                self._copy_to_archive(target_folder, obj)

            if not index % 10:
                logger.info(u"Archived %s of %s documents...", index, total)
                transaction.savepoint(optimistic=True)

        # 3. Copy DPEvent and Journals into snapshot
        copied_event = api.content.copy(self, target=archive)
        copied_event.Status = "closed"
        copied_event.reindexObject()

        # 4. Empty current Journals
        for journal in self.contentValues({'portal_type': 'Journal'}):
            adapter = IJournalEntryContainer(journal)
            for id, update in enumerate(adapter):
                adapter.delete(id)
            # Create message in old Journal to point to the new snapshot
            msg = u"Created snapshot of this event at {}".format(copied_event.absolute_url())
            adapter.add(JournalEntry(title="", text=msg))

        # local roles were set when adding items to the archive but reindexing was deferred.
        archive_contentarea.reindexObjectSecurity()

        logger.info(u"Finished snapshot of DPEvent %s", self.title)
        api.portal.show_message(_("Created snapshot of event."), REQUEST)
        return REQUEST.response.redirect(copied_event.absolute_url())

    def _ensureTargetFolder(self, obj, target):
        """
        Make sure that a personal or group folder with proper permissions
        exists for this document in the archive.
        """
        path = obj.getPhysicalPath()

        # 1. check whether this is a personal or a group document
        isGroup = "Groups" in path
        isTransfer = "Transfers" in path
        isMember = "Members" in path
        if isGroup:
            target = target.Groups
            container = self.content.Groups
            foldertype = "GroupFolder"
        elif isMember:
            target = target.Members
            container = self.content.Members
            foldertype = "UserFolder"
        elif isTransfer:
            target = target.Transfers
            container = self.content.Transfers
            foldertype = "DPTransferFolder"

        # 2. check for which user / group
        if isGroup or isTransfer or isMember:
            foldername = path[5]
        else:
            foldername = path[4]

        # 3. check for corresponding folder
        if foldername in target:
            if not isTransfer:
                mtool = api.portal.get_tool("portal_membership")
                mtool.setLocalRoles(target[foldername], [foldername], "Owner", reindex=False)
            return target[foldername]

        # 4. if it doesn't exist: create it
        old_parent = container.get(foldername)
        new = api.content.create(
            container=target,
            type=foldertype,
            id=foldername,
            title=old_parent.title,
            )

        # 5. and copy the local roles
        if not isTransfer:
            mtool = api.portal.get_tool("portal_membership")
            mtool.setLocalRoles(new, [foldername], "Owner", reindex=False)
        return new

    def can_move(self, obj):
        try:
            scns = IELANDocument(obj).scenarios
        except BaseException:
            # Object could have lost its ELAN behavior but that means we can
            # potentially delete it
            scns = ['dummy']
        apps = ILocalBehaviorSupport(obj).local_behaviors
        if len(scns) == 1 and len(apps) == 1:
            return True
        return False

    def _move_to_archive(self, target_folder_obj, obj):
        logger.info(
            u"Moving %s with %s attachments to %s",
            obj.absolute_url(),
            len(obj.keys()),
            target_folder_obj.absolute_url())

        mdate = obj.modified()
        transfer_events = obj.doc_extension(TRANSFERS_APP).transferEvents()
        moved_obj = api.content.move(obj, target_folder_obj)

        # Now do some repairs
        moved_obj.scenarios = []
        moved_obj.setModificationDate(mdate)
        # transferLog for archived items needs to be a string
        moved_obj.transferLog = str(transfer_events)
        moved_obj.reindexObject()

    def _copy_to_archive(self, target_folder_obj, obj):
        logger.info(
            u"Copying %s with %s attachments to %s",
            obj.absolute_url(),
            len(obj.keys()),
            target_folder_obj.absolute_url())

        copied_obj = api.content.copy(obj, target_folder_obj)

        # Now do some repairs
        mdate = obj.modified()
        copied_obj.scenarios = []

        wftool = api.portal.get_tool("portal_workflow")
        old_state = api.content.get_state(obj)
        if old_state == "published":
            wftool.doActionFor(copied_obj, "publish")
        elif old_state == "pending":
            wftool.doActionFor(copied_obj, "submit")

        copied_obj.setModificationDate(mdate)
        # transferLog for archived items needs to be a string
        events = obj.doc_extension(TRANSFERS_APP).transferEvents()
        copied_obj.transferLog = str(events)
        copied_obj.reindexObject()

        # Cleanup original DPDocument
        # 1. Remove current scenario
        scns = IELANDocument(obj).scenarios
        scns.remove(self.id)
        obj.scenarios = scns

        # 2. Remove elan behavior if there are no other events but other behaviors
        if not scns:
            apps = ILocalBehaviorSupport(obj).local_behaviors
            if len(apps) > 1:
                # There are others --> only remove ELAN behavior
                try:
                    apps.remove(ELAN_APP)
                    ILocalBehaviorSupport(obj).local_behaviors = list(set(apps))
                except Exception as e:
                    log_exc(e)
        obj.reindexObject()

    def _getDocumentsForScenario(self, **kwargs):
        """
        Collects all DPDocuments for the current scenario
        :return: list of brains
        """
        #        args = {'object_provides':IDPDocument.__identifier__, 'scenarios': self.getId()}
        args = {'portal_type': "DPDocument", 'scenarios': self.getId()}
        args.update(kwargs)
        return api.content.find(**args)

    def _createArchive(self):
        """
        We create an archive object. Into it, we copy the complete ESD hierarchy.
        We also create two folders "Members" and "Groups", which will hold all the
        documents for the scenario.
        """
        archive = self.archive  # Acquire root for archives
        esd = self.esd  # Acquire esd root
        now = safe_unicode(self.toLocalizedTime(DateTime(), long_format=1))
        id = ploneId(self, "%s_%s" % (self.getId(), now))
        title = u"%s %s" % (safe_unicode(self.Title()), now)
        # create the archive root
        arc = api.content.create(
            container=archive,
            type="ELANArchive",
            id=id,
            title=title,
            )
        arc.setDescription(self.Description())
        # create the document folders
        createPloneObjects(arc, ARCHIVESTRUCTURE)
        createPloneObjects(arc.content, TRANSFER_AREA)

        navSettings(arc)

        # copy the ESD folders
        for brain in esd.getFolderContents({'portal_type': ['ELANSection', 'ELANDocCollection']}):
            api.content.copy(brain.getObject(), arc.esd)
        arc.esd.setDefaultPage("overview")

        return arc

    def selectGlobally(self):
        global_scenarios = get_global_scenario_selection()
        global_scenarios[self.getId()] = 'selected'

    def createDefaultJournals(self):
        """
        Creates journals inside the event
        :return: """
        if not self.Journals:
            return
        docpool = self.myDocumentPool()
        prefix = docpool.prefix or docpool.getId()
        for index, title in enumerate(self.Journals, start=1):
            title = title.strip()
            # Skip empty lines
            if not title:
                continue
            journal_id = 'journal{}'.format(str(index))
            # Skip if it already exists
            if self.get(journal_id):
                pass
            journal = api.content.create(
                container=self,
                type='Journal',
                title=title,
                id=journal_id,
                )
            # Grant local role to Journal Editor Groups
            api.group.grant_roles(
                groupname='{}_Journal{}_Editors'.format(prefix, index),
                roles=['JournalEditor'],
                obj=journal,
                )
            # Grant local role to Journal Reader Groups
            api.group.grant_roles(
                groupname='{}_Journal{}_Readers'.format(prefix, index),
                roles=['JournalReader'],
                obj=journal,
                )


    def deleteEventReferences(self):
        """
        """
        self.Substitute = None
        self.reindexObject()

    def canBeAssigned(self):
        """
        Can this scenario be assigned to documents?
        Is it published? Is it active?
        """
        wftool = getToolByName(self, 'portal_workflow')
        return (
            wftool.getInfoFor(self, 'review_state') == 'published'
            and self.Status == 'active'
        )

    def bounds(self, fieldname='AreaOfInterest'):
        coordinates = self.coordinates(fieldname)
        if not coordinates:
            return
        return coordinates.bounds

    def coordinates(self, fieldname='EventCoordinates'):
        wkt = getattr(self, fieldname, None)
        if not wkt:
            return
        return geometry.from_wkt(wkt)

    def event_type_title(self):
        vocab = getUtility(Interface, name='docpool.event.vocabularies.EventTypes')
        return vocab(self).getTerm(self.EventType).title


class ELANScenario(DPEvent):
    pass


@adapter(IDPEvent, IObjectAddedEvent)
def eventAdded(obj, event=None):
    """
    For new scenarios, add them to each user's personal selection and
    create the journals.
    """
    if obj.isArchive():
        return
    obj.selectGlobally()
    obj.createDefaultJournals()


def addLogEntry(obj):
    changelog = json.loads(obj.changelog or '[]')
    entry = {}
    entry[u'Date'] = api.portal.get_localized_time(
        datetime.datetime.now(), long_format=1)
    entry[u'User'] = obj._getUserInfoString()
    entry[u'Status'] = obj.Status
    entry[u'EventType'] = obj.EventType
    entry[u'Operation mode'] = obj.OperationMode
    entry[u'Alerting status'] = obj.AlertingStatus
    entry[u'Alerting note'] = obj.AlertingNote
    entry[u'Phase'] = obj.phaseInfo()
    entry[u'Sectorizing sample types'] = u", ".join(
        obj.SectorizingSampleTypes
        if obj.SectorizingSampleTypes is not None else ' ')
    entry[u'Sectorizing networks'] = u", ".join(
        (n.to_object.title for n in obj.SectorizingNetworks)
        if obj.SectorizingNetworks is not None else ' ')
    # Check if there are changes to prevent duplicate log entries.
    if changelog and entry == changelog[-1]:
        return
    changelog.append(entry)
    obj.changelog = json.dumps(changelog)


@adapter(IDPEvent, IObjectModifiedEvent)
def eventChanged(obj, event=None):
    """
    """
    addLogEntry(obj)

    if obj.Status != 'active':
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
            args = {'portal_type': 'DPDocument', 'path': mpath}
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
            event.object):
        return
    if obj.id == 'routinemode':
        raise RuntimeError(u'The "routinemode" event cannot be removed.')

    global_scenarios = get_global_scenario_selection()
    global_scenarios[obj.getId()] = 'removed'


@adapter(IDPEvent, IActionSucceededEvent)
def eventPublished(obj, event=None):
    if event.__dict__['action'] == 'publish':
        # Update all objects for this scenario
        m = obj.content
        mpath = "/".join(m.getPhysicalPath())
        args = {'portal_type': 'DPDocument', 'path': mpath}
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
