from Acquisition import aq_base
from Acquisition import aq_get
from Acquisition import aq_inner
from Acquisition import aq_parent
from docpool.base import DocpoolMessageFactory as _
from docpool.base.content.archiving import IArchiving
from docpool.base.marker import IImportingMarker
from plone import api
from plone.autoform import directives
from plone.base.utils import safe_text
from plone.dexterity.interfaces import IEditFinishedEvent
from plone.supermodel import model
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import base_hasattr
from Products.DCWorkflow.interfaces import IAfterTransitionEvent
from zope import schema
from zope.component import adapter
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.interface import provider
from zope.lifecycleevent import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectCopiedEvent
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from zope.schema.interfaces import IContextAwareDefaultFactory

import datetime


@provider(IContextAwareDefaultFactory)
def initializeMdate(context):
    return context.created().asdatetime().replace(tzinfo=None) or datetime.datetime.now()


class IContentBase(model.Schema):
    """ """

    created_by = schema.TextLine(
        title=_("label_contentbase_created_by", default="Created by"),
        description=_("description_contentbase_created_by", default=""),
        required=False,
    )
    directives.omitted("created_by")

    modified_by = schema.TextLine(
        title=_("label_contentbase_modified_by", default="Modified by"),
        description=_("description_contentbase_modified_by", default=""),
        required=False,
    )
    directives.omitted("modified_by")

    mdate = schema.Datetime(
        title=_("label_contentbase_mdate", default="Date of last user action"),
        description=_("description_contentbase_mdate", default=""),
        required=False,
        defaultFactory=initializeMdate,
    )
    directives.omitted("mdate")

    wdate = schema.Datetime(
        title=_("label_contentbase_wdate", default="Date of last workflow action"),
        description=_("description_contentbase_wdate", default=""),
        required=False,
    )
    directives.omitted("wdate")


@implementer(IContentBase)
class ContentBase:
    """Mixin used by DPDocument, FolderBase, InfoLink, Text, DPEvent and SRTextBlock."""

    def _getUserInfoString(self, plain=False):
        from docpool.base.utils import getUserInfo

        userid, fullname, primary_group = getUserInfo(self)
        # print userid, fullname, primary_group
        res = safe_text(fullname)
        if primary_group:
            if plain:
                res += " %s" % safe_text(primary_group)
            else:
                res += " <i>%s</i>" % safe_text(primary_group)
        return res

    def getWdate(self):
        """ """
        return self.wdate

    def update_created(self):
        """ """
        self.created_by = self._getUserInfoString()

    def getMdate(self):
        """ """
        return (base_hasattr(self, "mdate") and self.mdate) or self.created().asdatetime().replace(
            tzinfo=None
        )

    def changed(self):
        """Overridden for transferable content."""
        return self.getMdate()

    def update_modified(self):
        """ """
        # print "update_modified"
        self.modified_by = self._getUserInfoString()
        self.mdate = datetime.datetime.now()
        self.reindexObject()

    def update_workflow(self):
        self.wdate = datetime.datetime.now()
        self.reindexObject()

    def modInfo(self, show_created=False):
        """ """
        cdate = self.CreationDate()
        mdate = self.mdate
        cby = self.created_by
        mby = self.modified_by

        if (not mby) or show_created:
            return cdate, cby
        else:
            return mdate, mby

    def isInGroupFolder(self):
        """
        Checks if the content has been created in a group folder.
        """
        return "Groups" in self.getPhysicalPath() or "Transfers" in self.getPhysicalPath()

    def myGroup(self):
        """Return the title of nearest group-folder.
        It's ok to use unrestrictedTraverse here, because we only return the title.
        TODO: The name and logic of this is not very clear.
        """
        pp = self.getPhysicalPath()
        if "Groups" in pp:
            i = pp.index("Groups")
            return self.unrestrictedTraverse("/".join(pp[: i + 2])).title
        else:
            return "Transfers"

    def createActions(self):
        """
        For override
        """

    def updateSecurity(self):
        """
        For dynamic placeful workflow settings
        """
        wtool = getToolByName(self, "portal_workflow")
        # wtool.updateRoleMappings(context)    # passing context is not possible :(
        #
        # Since WorkflowTool.updateRoleMappings()  from the line above supports
        # only sitewide updates code from updateRoleMappings() was copied below
        # to enable context passing to wftool._recursiveUpdateRoleMappings()
        wfs = {}
        for id in wtool.objectIds():
            wf = wtool.getWorkflowById(id)
            if hasattr(aq_base(wf), "updateRoleMappingsFor"):
                wfs[id] = wf
        context = aq_parent(aq_inner(self))
        wtool._recursiveUpdateRoleMappings(context, wfs)


@adapter(IContentBase, IObjectAddedEvent)
def updateCreated(obj, event=None):
    request = getRequest()
    if request is None:
        # fallback for failing test
        request = aq_get(obj, "REQUEST")
    if IImportingMarker.providedBy(request):
        return
    if request.get("creating", False):
        # print "#" * 20, "creating"
        if not IArchiving(obj).is_archive:
            obj.update_created()
        obj.createActions()


# edited
@adapter(IContentBase, IEditFinishedEvent)
# Edit was finished and contents are saved. This event is fired
#    even when no changes happen (and no modified event is fired.)
def updateModified(obj, event=None):
    if not IArchiving(obj).is_archive:
        obj.update_modified()


@adapter(IContentBase, IObjectCreatedEvent)
def markCreateEvent(obj, event):
    if IObjectCopiedEvent.providedBy(event):
        return
    if IImportingMarker.providedBy(getRequest()):
        return

    context = api.portal.get()
    request = context.REQUEST
    request.set("creating", True)


@adapter(IContentBase, IAfterTransitionEvent)
# Edit was finished and contents are saved. This event is fired
#    even when no changes happen (and no modified event is fired.)
def updateWorkflow(obj, event=None):
    if IImportingMarker.providedBy(getRequest()):
        return
    if not IArchiving(obj).is_archive:
        obj.update_workflow()
