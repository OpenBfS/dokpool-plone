# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from Acquisition import aq_base
from DateTime import DateTime
from docpool.base.content.contentbase import ContentBase
from docpool.base.content.contentbase import IContentBase
from docpool.base.utils import portalMessage
from docpool.config.local.base import navSettings
from docpool.config.local.elan import ARCHIVESTRUCTURE
from docpool.config.local.transfers import TRANSFER_AREA
from docpool.config.utils import createPloneObjects
from docpool.config.utils import ploneId
from docpool.event import DocpoolMessageFactory as _
from docpool.localbehavior.localbehavior import ILocalBehaviorSupport
from docpool.transfers.config import TRANSFERS_APP
from five import grok
from logging import getLogger
from plone.app.textfield import RichText
from plone.app.textfield import RichTextValue
from plone.autoform import directives
from plone.dexterity.content import Item
from plone.dexterity.utils import safe_unicode
from plone.directives import form
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.protect.interfaces import IDisableCSRFProtection
from Products.Archetypes.utils import DisplayList
from Products.CMFCore.interfaces import IActionSucceededEvent
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.i18nl10n import utranslate
from Products.CMFPlone.utils import log
from Products.CMFPlone.utils import log_exc
from Products.CMFPlone.utils import parent
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.component import adapter
from zope.interface import alsoProvides
from zope.interface import implements
from zope.lifecycleevent.interfaces import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.schema.interfaces import IContextSourceBinder

import datetime


logger = getLogger("dpevent")


@grok.provider(IContextSourceBinder)
def availableScenarios(context):
    if hasattr(context, "dpSearchPath"):
        path = context.dpSearchPath() + "/contentconfig/scen"
    else:
        path = "/Plone/contentconfig/scen"
    query = {"portal_type": ["DPEvent"], "path": {'query': path}}

    return ObjPathSourceBinder(
        navigation_tree_query=query, object_provides=IDPEvent.__identifier__
    ).__call__(context)


class IDPEvent(form.Schema, IContentBase):
    """
    """

    Status = schema.Choice(
        title=_(u'label_dpevent_status', default=u'Status of the scenario'),
        description=_(u'description_dpevent_status', default=u''),
        required=True,
        source="docpool.base.vocabularies.Status",
    )

    Exercise = schema.Bool(
        title=_(u'label_dpevent_exercise', default=u'Is this an exercise?'),
        description=_(u'description_dpevent_exercise', default=u''),
        required=False,
    )

    TimeOfEvent = schema.Datetime(
        title=_(u'label_dpevent_timeofevent', default=u'Time of event'),
        description=_(u'description_dpevent_timeofevent', default=u''),
        required=True,
    )

    Substitute = RelationChoice(
        title=_(u'label_dpevent_substitute', default=u'Substitute scenario'),
        description=_(
            u'description_dpevent_substitute',
            default=u'Only relevant for private scenarios received from another organisation. Allows you map content for this scenario to one of you own scenarios.',
        ),
        required=False,
        source="docpool.event.vocabularies.EventSubstitutes",
    )
    form.widget(Substitute='z3c.form.browser.select.SelectFieldWidget')

    # directives.widget(ScenarioPhase=AutocompleteFieldWidget)
    directives.widget(ScenarioPhase='z3c.form.browser.select.SelectFieldWidget')
    ScenarioPhase = RelationChoice(
        title=_(u"Scenario & Phase"),
        vocabulary=u"docpool.event.vocabularies.Phases",
        required=False,
    )

    directives.widget(ScenarioLocation='z3c.form.browser.select.SelectFieldWidget')
    ScenarioLocation = RelationChoice(
        title=_(u'Scenario location'),
        vocabulary=u"docpool.event.vocabularies.PowerStations",
        required=False,
    )

    ScenarioCoordinates = schema.TextLine(
        title=_(u'Scenario coordinates'), required=False
    )

    OperationMode = schema.Choice(
        title=_(u'Operation mode'),
        vocabulary=u"docpool.event.vocabularies.Modes",
        required=False,
    )

    SectorizingSampleTypes = schema.List(
        title=_(u'Sectorizing sample types'),
        required=False,
        value_type=schema.Choice(source=u"docpool.event.vocabularies.SampleTypes"),
    )

    directives.widget(
        SectorizingNetworks='z3c.form.browser.select.CollectionSelectFieldWidget'
    )
    SectorizingNetworks = RelationList(
        title=_(u'Sectorizing networks'),
        required=False,
        value_type=RelationChoice(source=u'docpool.event.vocabularies.Networks'),
    )

    AreaOfInterest = schema.Text(title=_(u"Area of interest"), required=False)

    changelog = RichText(
        title=_(u'label_dpevent_changelog', default=u'Changelog'),
        description=_(u''),
        required=False,
        readonly=True,
    )


@form.default_value(field=IDPEvent['TimeOfEvent'])
def initializeTimeOfEvent(data):
    # To get hold of the folder, do: context = data.context
    return datetime.datetime.today()


class DPEvent(Item, ContentBase):
    """
    """

    security = ClassSecurityInfo()

    implements(IDPEvent)

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
        if self.ScenarioPhase:
            return self.ScenarioPhase.to_object.getPhaseTitle()
        return ""

    def getStates(self):
        """
        """
        return DisplayList(
            [
                ('active', _('active')),
                ('inactive', _('inactive')),
                ('closed', _('closed')),
            ]
        )

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
        self.snapshot()
        self.purge()
        self.Status = 'closed'
        self.reindexObject()
        portalMessage(self, _("Scenario archived"), "info")
        return self.restrictedTraverse("view")()

    security.declareProtected("Modify portal content", "snapshot")

    def snapshot(self, REQUEST=None):
        """
        Saves all content for this scenario to a new archive, but does not delete any files.
        Status is unchanged.
        """
        alsoProvides(REQUEST or self.REQUEST, IDisableCSRFProtection)
        arc = self._createArchiveFolders()
        # TODO
        m = self.content
        mpath = "/".join(m.getPhysicalPath())
        arc_m = arc.content
        # We now query the catalog for all documents belonging to this scenario within
        # the personal and group folders
        mdocs = self._getDocumentsForScenario(path=mpath)
        for doc in mdocs:
            target_folder = self._ensureTargetFolder(doc, arc_m)
            self._copyDocument(target_folder, doc)
        if REQUEST:
            portalMessage(self, _("Snapshot created"), "info")
            return self.restrictedTraverse("view")()

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
            mtool.setLocalRoles(af, [fname], 'Owner')
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
            new_id = result[0]['new_id']
            copied_obj = target_folder_obj._getOb(new_id)
            mdate = source_obj.modified()
            copied_obj.scenarios = []
            wf_state = source_brain.review_state
            wftool = getToolByName(self, 'portal_workflow')
            # print wf_state, wftool.getInfoFor(copied_obj, 'review_state')
            if (
                wf_state == "published"
                and wftool.getInfoFor(copied_obj, 'review_state') != 'published'
            ):
                wftool.doActionFor(copied_obj, 'publish')
            if (
                wf_state == "pending"
                and wftool.getInfoFor(copied_obj, 'review_state') == 'private'
            ):
                wftool.doActionFor(copied_obj, 'submit')
            copied_obj.setModificationDate(mdate)
            events = source_obj.doc_extension(TRANSFERS_APP).transferEvents()
            copied_obj.transferLog = str(events)
            copied_obj.reindexObject()
            copied_obj.reindexObjectSecurity()
        else:
            log("Could not archive %s" % source_obj.absolute_url())

    def _getDocumentsForScenario(self, **kwargs):
        """
        Helper function for catalog queries
        """
        #        args = {'object_provides':IDPDocument.__identifier__, 'scenarios': self.getId()}
        args = {'portal_type': "DPDocument", 'scenarios': self.getId()}
        args.update(kwargs)
        cat = getToolByName(self, "portal_catalog")
        return cat(args)

    def _createArchiveFolders(self):
        """
        We create an archive object. Into it, we copy the complete ESD hierarchy.
        We also create two folders "Members" and "Groups", which will hold all the
        documents for the scenario.
        """
        a = self.archive  # Acquire root for archives
        e = self.esd  # Acquire esd root
        now = safe_unicode(self.toLocalizedTime(DateTime(), long_format=1))
        id = ploneId(self, "%s_%s" % (self.getId(), now))
        title = u"%s %s" % (safe_unicode(self.Title()), now)
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
                {'portal_type': ['ELANSection', 'ELANDocCollection']}
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
        from docpool.elan.config import ELAN_APP
        from docpool.elan.behaviors.elandocument import IELANDocument

        source_obj = source_brain.getObject()
        # determine parent folder for copy
        scns = None
        try:
            scns = IELANDocument(source_obj).scenarios
        except:
            # Object could have lost its ELAN behavior but that means we can potentially delete it
            scns = ['dummy']
        if len(scns) == 1:  # only the one scenario --> potential delete
            # Check for other applications than ELAN
            apps = ILocalBehaviorSupport(source_obj).local_behaviors
            if apps and len(apps) > 1:  # There are others --> only remove ELAN behavior
                try:
                    apps.remove(ELAN_APP)
                    ILocalBehaviorSupport(source_obj).local_behaviors = list(set(apps))
                except Exception, e:
                    log_exc(e)
            else:  # we delete
                p = parent(source_obj)
                p.manage_delObjects([source_obj.getId()])
        else:  # Only remove the scenario
            scns = list(scns)
            scns.remove(self.getId())
            source_obj.scenarios = scns
            source_obj.reindexObject()

    def addScenarioForUsers(self):
        """
        Add this scenario to each users selection of scenarios.
        """
        pm = getToolByName(self, 'portal_membership')
        # TODO: nur für die eigenen Nutzer
        for memberId in pm.listMemberIds():
            member = pm.getMemberById(memberId)
            scns = list(member.getProperty("scenarios"))
            if self.getId() not in scns:
                scns.append(self.getId())
            member.setMemberProperties({"scenarios": scns})

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


class ELANScenario(DPEvent):
    pass


@adapter(IDPEvent, IObjectAddedEvent)
def eventAdded(obj, event=None):
    """
    For new scenarios, add them to each user's personal selection.
    """
    # print "scenarioAdded"
    obj.addScenarioForUsers()


def addLogEntry(old_changelog, obj):
    print obj.SectorizingNetworks
    mdate, userInfo = obj.modInfo()
    text = """
    <tr>
    <td>%s<br/>(%s)</td>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
    </tr>
    <tr class="last"></tr>
    """ % (
        obj.toLocalizedTime(mdate, long_format=1),
        userInfo,
        obj.Status,
        obj.OperationMode,
        obj.phaseInfo(),
        ", ".join(
            obj.SectorizingSampleTypes if obj.SectorizingSampleTypes != None else ' '
        ),
        ", ".join(
            (n.to_object.Title() for n in obj.SectorizingNetworks)
            if obj.SectorizingNetworks != None
            else ' '
        ),
    )
    new_changelog = old_changelog.replace(
        """<tr class="last"></tr>""", safe_unicode(text)
    )
    obj.changelog = RichTextValue(new_changelog, 'text/html', 'text/html')


@adapter(IDPEvent, IObjectModifiedEvent)
def eventChanged(obj, event=None):
    """
    """
    # print 'eventChanged'
    # write changelog
    old_changelog = """
    <table>
    <thead>
    <tr>
    <th>%s</th>
    <th>%s</th>
    <th>%s</th>
    <th>%s</th>
    <th>%s</th>
    <th>%s</th>
    </tr>
    </thead>
    <tbody>
    <tr class="last"></tr>
    </tbody>
    </table>
    """ % (
        _(u"Date"),
        _(u"Status"),
        _(u"Operation mode"),
        _(u"Phase"),
        _(u"Sectorizing sample types"),
        _(u"Sectorizing networks"),
    )
    if obj.changelog:
        old_changelog = safe_unicode(obj.changelog.output)

    addLogEntry(old_changelog, obj)

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
                except Exception, e:
                    log_exc(e)


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
            except Exception, e:
                log_exc(e)
