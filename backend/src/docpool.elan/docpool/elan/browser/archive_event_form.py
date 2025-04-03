from Acquisition import aq_get
from datetime import datetime
from docpool.base.config import TRANSFERS_APP
from docpool.base.content.archiving import IArchiving
from docpool.base.localbehavior.localbehavior import ILocalBehaviorSupport
from docpool.config.local.base import navSettings
from docpool.config.local.elan import ARCHIVESTRUCTURE
from docpool.config.local.transfers import TRANSFER_AREA
from docpool.config.utils import createPloneObjects
from docpool.config.utils import ploneId
from docpool.elan import DocpoolMessageFactory as _
from docpool.elan.behaviors.elandocument import IELANDocument
from docpool.elan.config import ELAN_APP
from docpool.elan.utils import get_global_scenario_selection
from elan.journal.adapters import IJournalEntryContainer
from logging import getLogger
from plone import api
from Products.CMFPlone.utils import log_exc
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.i18nmessageid import MessageFactory

import transaction
import uuid


logger = getLogger(__name__)
PMF = MessageFactory("plone")


class Archive(BrowserView):
    def __call__(self):
        request = self.request
        if IArchiving(self.context).is_archive:
            logger.info("Item is already archived!")
            return request.response.redirect(self.context.absolute_url())

        form = self.request.form
        if form.get("form.uid"):
            self.uid = form.get("form.uid")
        else:
            self.uid = str(uuid.uuid4())
        self.action = self.__name__

        contentarea = aq_get(self.context, "content")
        contentarea_path = "/".join(contentarea.getPhysicalPath())
        self.items = self._getDocumentsForScenario(path=contentarea_path)

        archiving_info = self.context.get_archiving_info()
        if (
            archiving_info
            and self.uid in archiving_info
            and archiving_info[self.uid]["state"] != "completed"
        ):
            # Most likely reloading the form after the process started.
            # Reasons:
            # * There was a timeout or a guru-meditation-error and Users wants to start again.
            # * User is impatient :)
            # We tell people to wait a bit longer.
            msg = _(
                "Item being archived right now! Please try again in a couple of minutes."
            )
            logger.info(msg)
            logger.info(archiving_info)
            api.portal.show_message(msg, self.request)
            return self.index()

        elif archiving_info and self.uid not in archiving_info:
            # We have old archiving-info for one of these reasons:
            # * A previous snapshot was finished (ok, maybe display and show link to it?)
            # * A archiving-process is still running
            # * The archiving process was interrupted by a traceback or restart
            # TODO: How should we handele these cases?
            msg = _("Item has old archiving info!")
            logger.info(msg)
            logger.info(archiving_info)
            api.portal.show_message(msg, self.request)

        if form.get("form.button.cancel"):
            msg = PMF("Changes canceled.")
            api.portal.show_message(msg, self.request)
            return request.response.redirect(self.context.absolute_url())

        if not form.get("form.button.submit", None):
            return self.index()

        # Create and store info
        info = {}
        info[self.uid] = {
            "user": api.user.get_current().getId(),
            "time": datetime.now(),
            "action": self.action,
            "state": "in_progress",
        }
        self.context.set_archiving_info(info)
        # We commit to make the state of the event being archived available before archiving is finished
        transaction.commit()

        target = self.process_action()

        # Mark as completed
        info[self.uid]["state"] = "completed"
        self.context.set_archiving_info(info)

        request.response.redirect(target.absolute_url())

    def process_action(self):
        """
        Saves all content for this scenario to an archive, deletes the original content,
        and sets the scenario to state "closed".

        This can take a long time since associated DPDocuments can have many attechments
        and all need to be copied or moved and reindexed. This is why we make savepoints.
        """

        # 1. Disable scenario to prevent new data from being added for it
        global_scenarios = get_global_scenario_selection()
        global_scenarios[self.context.UID()] = "closed"
        self.context.Status = "closed"
        transaction.savepoint(optimistic=True)

        # 2. Create Archive
        archive = self._createArchive()
        archive_contentarea = archive.content
        logger.info(
            "Archiving DPEvent %s to %s", self.context.title, archive.absolute_url()
        )
        contentarea = aq_get(self.context, "content")
        contentarea_path = "/".join(contentarea.getPhysicalPath())

        # 3. Move or Copy related DPDocuments
        brains = self._getDocumentsForScenario(path=contentarea_path)
        total = len(brains)
        logger.info(
            "Archiving %s items associated with DPEvent %s. This may take a while...",
            total,
            self.context.absolute_url(),
        )
        for index, brain in enumerate(brains, start=1):
            obj = brain.getObject()
            target_folder = self._ensureTargetFolder(obj, archive_contentarea)
            if self.can_move(obj):
                self._move_to_archive(target_folder, obj)
            else:
                self._copy_to_archive(target_folder, obj)

            if not index % 10:
                logger.info("Archived %s of %s documents...", index, total)
                transaction.savepoint(optimistic=True)

        # 4. Move DPEvent into archive and redirect to it
        archived_event = api.content.move(self.context, target=archive)
        archived_event.reindexObject()
        # local roles were set when adding items to the archive but reindexing was deferred.
        archive_contentarea.reindexObjectSecurity()
        logger.info("Finished archiving DPEvent %s", archived_event.title)
        api.portal.show_message(_("Scenario archived"), self.request)
        return archived_event

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
            container = self.context.content.Groups
            foldertype = "GroupFolder"
        elif isMember:
            target = target.Members
            container = self.context.content.Members
            foldertype = "UserFolder"
        elif isTransfer:
            target = target.Transfers
            container = self.context.content.Transfers
            foldertype = "DPTransferFolder"

        # 2. check for which user / group
        foldername = path[5] if isGroup or isTransfer or isMember else path[4]

        # 3. check for corresponding folder
        if foldername in target:
            if not isTransfer:
                mtool = api.portal.get_tool("portal_membership")
                mtool.setLocalRoles(
                    target[foldername], [foldername], "Owner", reindex=False
                )
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
            localroles = getattr(old_parent, "__ac_local_roles__", [])
            if localroles:
                for userid in localroles:
                    new.manage_setLocalRoles(userid=userid, roles=localroles[userid])
            block = getattr(old_parent, "__ac_local_roles_block__", False)
            if block:
                new.__ac_local_roles_block__ = block

        return new

    def can_move(self, obj):
        try:
            scns = IELANDocument(obj).scenarios
        except BaseException:
            # Object could have lost its ELAN behavior but that means we can
            # potentially delete it
            scns = ["dummy"]
        # Ignore duplicates!
        apps = set(ILocalBehaviorSupport(obj).local_behaviors)
        return bool(len(scns) == 1 and len(apps) == 1)

    def _move_to_archive(self, target_folder_obj, obj):
        logger.info(
            "Moving %s with %s attachments to %s",
            obj.absolute_url(),
            len(obj.keys()),
            target_folder_obj.absolute_url(),
        )

        mdate = obj.modified()
        transfer_events = obj.doc_extension(TRANSFERS_APP).transferEvents()
        old_state = api.content.get_state(obj)
        moved_obj = api.content.move(obj, target_folder_obj)
        new_state = api.content.get_state(moved_obj)

        if old_state != new_state:
            # We directly transition for speed
            wftool = api.portal.get_tool("portal_workflow")
            if old_state == "published" and new_state in ["private", "pending"]:
                wftool.doActionFor(moved_obj, "publish")
            elif old_state == "pending" and new_state in ["private"]:
                wftool.doActionFor(moved_obj, "submit")
            elif old_state == "pending" and new_state in ["published"]:
                wftool.doActionFor(moved_obj, "retract")
            else:
                # See https://redmine-koala.bfs.de/issues/5007
                api.content.transition(moved_obj, to_state=old_state)

        # Now do some repairs
        moved_obj.scenarios = []
        moved_obj.setModificationDate(mdate)
        # transferLog for archived items needs to be a string
        moved_obj.transferLog = str(transfer_events)
        moved_obj.reindexObject(idxs=["modified", "review_state", "scenarios"])

    def _copy_to_archive(self, target_folder_obj, obj):
        logger.info(
            "Copying %s with %s attachments to %s",
            obj.absolute_url(),
            len(obj.keys()),
            target_folder_obj.absolute_url(),
        )

        copied_obj = api.content.copy(obj, target_folder_obj)

        # Now do some repairs
        mdate = obj.modified()
        copied_obj.scenarios = []

        old_state = api.content.get_state(obj)
        new_state = api.content.get_state(copied_obj)

        if old_state != new_state:
            # We directly transition for speed
            wftool = api.portal.get_tool("portal_workflow")
            if old_state == "published" and new_state in ["private", "pending"]:
                wftool.doActionFor(copied_obj, "publish")
            elif old_state == "pending" and new_state in ["private"]:
                wftool.doActionFor(copied_obj, "submit")
            elif old_state == "pending" and new_state in ["published"]:
                wftool.doActionFor(copied_obj, "retract")
            else:
                # See https://redmine-koala.bfs.de/issues/5007
                api.content.transition(copied_obj, to_state=old_state)

        copied_obj.setModificationDate(mdate)
        # transferLog for archived items needs to be a string
        events = obj.doc_extension(TRANSFERS_APP).transferEvents()
        copied_obj.transferLog = str(events)
        copied_obj.reindexObject(idxs=["modified", "review_state", "scenarios"])

        # Cleanup original DPDocument
        # 1. Remove current scenario
        scns = IELANDocument(obj).scenarios
        # Drop duplicates
        scns = list(set(scns))
        scns.remove(self.context.UID())
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
        obj.reindexObject(idxs=["apps_supported", "scenarios"])

    def _getDocumentsForScenario(self, **kwargs):
        """
        Collects all DPDocuments for the current scenario
        :return: list of brains
        """
        #        args = {'object_provides':IDPDocument.__identifier__, 'scenarios': self.getId()}
        args = {
            "portal_type": "DPDocument",
            "scenarios": self.context.UID(),
            "sort_on": "sortable_title",
        }
        args.update(kwargs)
        return api.content.find(**args)

    def _createArchive(self):
        """
        We create an archive object. Into it, we copy the complete ESD hierarchy.
        We also create two folders "Members" and "Groups", which will hold all the
        documents for the scenario.
        """
        archive = aq_get(self.context, "archive")  # Acquire root for archives
        esd = self.context.esd  # Acquire esd root
        now = self.context.toLocalizedTime(datetime.now(), long_format=1)
        # create the archive root
        arc = api.content.create(
            container=archive,
            type="ELANArchive",
            id=ploneId(self.context, f"{self.context.id}_{now}"),
            title=f"{self.context.title} {now}",
        )
        arc.description = self.context.description
        # create the document folders
        createPloneObjects(arc, ARCHIVESTRUCTURE)
        createPloneObjects(arc.content, TRANSFER_AREA)

        navSettings(arc)

        # copy the ESD folders
        for brain in api.content.find(
            context=esd, portal_type=["ELANSection", "ELANDocCollection"]
        ):
            api.content.copy(brain.getObject(), arc.esd)
        arc.esd.setDefaultPage("overview")

        return arc


class Snapshot(Archive):
    def process_action(self):
        """
        Similar to archiveAndClose but leave the old event as is.
        Previously this was two seperate actions snapshot & purge. But if content would be
        added between snapshop and purge that would be lost forever.

        * Create Archive for event but leave Event unchanged
        * Copy Journals and Event to Archive
        * Purge Journals
        * Purge Event (move content to archive unless used by other apps or events)
        """

        # 1. Create Archive
        archive = self._createArchive()
        archive_contentarea = aq_get(archive, "content")
        logger.info(
            "Create snapshot of DPEvent %s in %s",
            self.context.title,
            archive.absolute_url(),
        )

        # 2. Move or Copy related DPDocuments (previously done by purge)
        contentarea = aq_get(self.context, "content")
        contentarea_path = "/".join(contentarea.getPhysicalPath())
        brains = self._getDocumentsForScenario(path=contentarea_path)
        total = len(brains)
        logger.info(
            "Archiving %s items associated with DPEvent %s. This may take a while...",
            total,
            self.context.absolute_url(),
        )
        for index, brain in enumerate(brains, start=1):
            obj = brain.getObject()
            target_folder = self._ensureTargetFolder(obj, archive_contentarea)
            if self.can_move(obj):
                self._move_to_archive(target_folder, obj)
            else:
                self._copy_to_archive(target_folder, obj)

            if not index % 10:
                logger.info("Archived %s of %s documents...", index, total)
                transaction.savepoint(optimistic=True)

        # 3. Copy DPEvent and Journals into snapshot
        copied_event = api.content.copy(self.context, target=archive)
        copied_event.Status = "closed"
        copied_event.reindexObject()

        # 4. Empty current Journals and copy local roles
        for journal in self.context.contentValues({"portal_type": "Journal"}):
            adapter = IJournalEntryContainer(journal)
            for entry_id, _update in enumerate(adapter):
                adapter.delete(entry_id)
            # Copy local roles to journals
            copied_journal = copied_event[journal.id]
            copied_journal.__ac_local_roles__ = journal.__ac_local_roles__
            copied_journal._p_changed = True

        # local roles were set when adding items to the archive but reindexing was deferred.
        archive_contentarea.reindexObjectSecurity()

        logger.info("Finished snapshot of DPEvent %s", self.context.title)
        api.portal.show_message(_("Created snapshot of event."), self.request)
        return copied_event
