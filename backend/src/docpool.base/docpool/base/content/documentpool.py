from docpool.base import DocpoolMessageFactory as _
from docpool.base.appregistry import APP_REGISTRY
from docpool.base.appregistry import implicitApps
from docpool.base.config import BASE_APP
from docpool.base.content.doctype import IDocType
from docpool.base.events import DocumentPoolInitializedEvent
from docpool.base.events import DocumentPoolRemovedEvent
from docpool.base.marker import IImportingMarker
from persistent.list import PersistentList
from plone import api
from plone.app.textfield.value import RichTextValue
from plone.autoform import directives
from plone.base.interfaces.siteroot import IPloneSiteRoot
from plone.dexterity.content import Container
from plone.dexterity.interfaces import IEditFinishedEvent
from plone.namedfile.field import NamedBlobImage
from plone.protect.utils import safeWrite
from plone.supermodel import model
from Products.CMFCore.utils import getToolByName
from Products.ZCatalog.ProgressHandler import ZLogHandler
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.event import notify
from zope.globalrequest import getRequest
from zope.interface import implementer
from zope.lifecycleevent import IObjectAddedEvent
from zope.lifecycleevent import IObjectRemovedEvent


APPLICATIONS_KEY = "docpool_applications_key"


class IDocumentPool(model.Schema):
    """ """

    prefix = schema.TextLine(
        title=_("label_documentpool_prefix", default="Prefix names"),
        description=_(
            "description_documentpool_prefix",
            default="Will be used to construct user and group names. If left blank, the id of the ESD will be used. ",
        ),
        required=False,
    )

    customLogo = NamedBlobImage(
        title=_("label_documentpool_customlogo", default="Custom Logo"),
        description=_("description_documentpool_customlogo", default=""),
        required=False,
    )

    supportedApps = schema.List(
        title=_(
            "label_documentpool_supportedapps",
            default="Applications supported in this document pool",
        ),
        description=_("description_documentpool_supportedapps", default=""),
        required=False,
        missing_value=(),
        value_type=schema.Choice(source="docpool.base.vocabularies.SelectableApps"),
    )

    directives.widget(supportedApps=CheckBoxFieldWidget)


@implementer(IDocumentPool)
class DocumentPool(Container):
    """ """

    def logoSrc(self):
        if self.customLogo:
            return "%s/@@images/customLogo/preview" % self.absolute_url()
        else:
            return None

    def configure(self):
        """ """
        docPoolAdded(self, None)
        return self.restrictedTraverse("@@view")()

    def myPrefix(self):
        return self.prefix or self.getId()

    def reindexAll(self):
        """ """
        catalog = api.portal.get_tool("portal_catalog")
        pghandler = ZLogHandler(steps=5000)
        catalog.reindexIndex(
            [
                "dp_type",
                "apps_supported",
                "object_provides",
                "allowedRolesAndUsers",
            ],
            REQUEST=None,
            pghandler=pghandler,
        )

    def myDocumentTypes(self, ids_only=False):
        """ """
        cat = getToolByName(self, "portal_catalog")
        res = cat(
            path=self.dpSearchPath(),
            object_provides=IDocType.__identifier__,
            sort_on="getId",
        )
        if ids_only:
            return [dt.getId for dt in res]
        else:
            return [(dt.getId, dt.Title) for dt in res]

    def dpSearchPath(self):
        """ """
        return "/".join(self.getPhysicalPath())

    def deleteText(self, obj):
        """ """
        safeWrite(obj, self.REQUEST)
        obj.text = RichTextValue("", "text/plain", "text/html")

    def allSupportedApps(self):
        """
        For acquisition.
        @return:
        """
        return self.supportedApps

    def isActive(self, APP):
        dp_app_state = getMultiAdapter((self, self.REQUEST), name="dp_app_state")
        return dp_app_state.isCurrentlyActive(APP)

    def myDocumentPool(self):
        """ """
        return self


@adapter(IDocumentPool, IObjectAddedEvent)
def docPoolAdded(obj, event=None):
    """ """
    self = obj
    # initialize cache for enabled apps
    annotations = IAnnotations(self)
    if APPLICATIONS_KEY not in annotations:
        annotations[APPLICATIONS_KEY] = PersistentList()

    if IImportingMarker.providedBy(getRequest()):
        return
    # Trigger my own method
    APP_REGISTRY[BASE_APP]["dpAddedMethod"](self)
    # Trigger configs for all supported applications
    if self.supportedApps:
        for app in self.supportedApps:
            APP_REGISTRY[app]["dpAddedMethod"](self)
    for appdef in implicitApps():
        appdef[2]["dpAddedMethod"](self)
    notify(DocumentPoolInitializedEvent(self))


@adapter(IDocumentPool, IEditFinishedEvent)
def docPoolModified(obj, event=None):
    """
    The range of supportedApps might have changed. So we trigger initialization for all apps.
    The methods are required to support this repetitive pattern.
    @param obj:
    @param event:
    @return:
    """
    if IImportingMarker.providedBy(getRequest()):
        return
    self = obj
    # Trigger configs for all supported applications
    if self.supportedApps:
        for app in self.supportedApps:
            APP_REGISTRY[app]["dpAddedMethod"](self)
    for appdef in implicitApps():
        appdef[2]["dpAddedMethod"](self)


@adapter(IDocumentPool, IObjectRemovedEvent)
def docPoolRemoved(obj, event=None):
    """ """
    if IPloneSiteRoot.providedBy(event.object):
        return

    self = obj
    # Trigger my own method
    APP_REGISTRY[BASE_APP]["dpRemovedMethod"](self)
    # Trigger configs for all applications
    if self.supportedApps:
        for app in self.supportedApps:
            APP_REGISTRY[app]["dpRemovedMethod"](self)
    for appdef in implicitApps():
        appdef[2]["dpRemovedMethod"](self)
    notify(DocumentPoolRemovedEvent(self))
