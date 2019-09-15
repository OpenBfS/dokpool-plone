# -*- coding: utf-8 -*-
#
# File: documentpool.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the DocumentPool content type. See documentpool.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from docpool.base import DocpoolMessageFactory as _
from docpool.base.appregistry import APP_REGISTRY
from docpool.base.appregistry import implicitApps
from docpool.base.config import BASE_APP
from docpool.base.content.doctype import IDocType
from docpool.base.content.groupfolder import IGroupFolder
from docpool.base.events import DocumentPoolInitializedEvent
from docpool.base.events import DocumentPoolRemovedEvent
from persistent.list import PersistentList
from plone.app.textfield.value import RichTextValue
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.dexterity.interfaces import IEditFinishedEvent
from plone.supermodel import model
from plone.namedfile.field import NamedBlobImage
from plone.protect.utils import safeWrite
from Products.CMFCore.utils import getToolByName
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.event import notify
from zope.interface import implementer
from zope.lifecycleevent import IObjectAddedEvent
from zope.lifecycleevent import IObjectRemovedEvent

APPLICATIONS_KEY = 'docpool_applications_key'


class IDocumentPool(model.Schema):
    """
    """

    prefix = schema.TextLine(
        title=_(u'label_documentpool_prefix', default=u'Prefix names'),
        description=_(
            u'description_documentpool_prefix',
            default=u'Will be used to construct user and group names. If left blank, the id of the ESD will be used. ',
        ),
        required=False,
    )

    customLogo = NamedBlobImage(
        title=_(u'label_documentpool_customlogo', default=u'Custom Logo'),
        description=_(u'description_documentpool_customlogo', default=u''),
        required=False,
    )

    supportedApps = schema.List(
        title=_(
            u'label_documentpool_supportedapps',
            default=u'Applications supported in this document pool',
        ),
        description=_(u'description_documentpool_supportedapps', default=u''),
        required=False,
        missing_value=(),
        value_type=schema.Choice(
            source="docpool.base.vocabularies.SelectableApps"),
    )

    directives.widget(supportedApps=CheckBoxFieldWidget)


@implementer(IDocumentPool)
class DocumentPool(Container):
    """
    """

    security = ClassSecurityInfo()

    def logoSrc(self):
        if self.customLogo:
            return "%s/@@images/customLogo/preview" % self.absolute_url()
        else:
            return None

    def configure(self):
        """
        """
        docPoolAdded(self, None)
        return self.restrictedTraverse("@@view")()

    def myPrefix(self):
        return self.prefix or self.getId()

    def reindexAll(self):
        """
        """
        cat = getToolByName(self, "portal_catalog")
        res = cat(path=self.dpSearchPath())
        for r in res:
            o = r.getObject()
            if o:
                o.reindexObject()
                o.reindexObjectSecurity()

    def myDocumentTypes(self, ids_only=False):
        """
        """
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
        """
        """
        return "/".join(self.getPhysicalPath())

    def deleteText(self, obj):
        """
        """
        safeWrite(obj, self.REQUEST)
        obj.text = RichTextValue(u"", 'text/plain', 'text/html')

    def allSupportedApps(self):
        """
        For acquisition.
        @return:
        """
        return self.supportedApps

    def isActive(self, APP):
        dp_app_state = getMultiAdapter(
            (self, self.REQUEST), name=u'dp_app_state')
        return dp_app_state.isCurrentlyActive(APP)

    def myDocumentPool(self):
        """
        """
        return self

    def getFirstChild(self):
        """
        """
        fc = self.getFolderContents()
        if len(fc) > 0:
            return fc[0].getObject()
        else:
            return None

    def getAllContentObjects(self):
        """
        """
        return [obj.getObject() for obj in self.getFolderContents()]

    def getContentAreas(self, **kwargs):
        """
        """
        args = {'portal_type': 'ContentArea'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getDPConfigs(self, **kwargs):
        """
        """
        args = {'portal_type': 'DPConfig'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]


@adapter(IDocumentPool, IObjectAddedEvent)
def docPoolAdded(obj, event=None):
    """
    """
    self = obj
    # initialize cache for enabled apps
    annotations = IAnnotations(self)
    if APPLICATIONS_KEY not in annotations:
        annotations[APPLICATIONS_KEY] = PersistentList()

    # Trigger my own method
    APP_REGISTRY[BASE_APP]['dpAddedMethod'](self)
    # Trigger configs for all supported applications
    for app in self.supportedApps:
        APP_REGISTRY[app]['dpAddedMethod'](self)
    for appdef in implicitApps():
        appdef[2]['dpAddedMethod'](self)
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
    self = obj

    # We shouldn't really care about group folders in this piece of code.
    # Using events sounds better but would make it complicated to pass
    # information from before changing application support to afterwards.

    # Store locally allowed types on group folders for fixing immediately
    # addable types later in case editing supported applications changed
    # something about them.
    cat = getToolByName(self, "portal_catalog")
    group_folders = set(brain.getObject() for brain in cat(
        path=self.dpSearchPath(),
        object_provides=IGroupFolder.__identifier__,
    ))
    allowed_before = {
        gf: gf.get_locally_allowed_types() for gf in group_folders}

    # Trigger configs for all supported applications
    if self.supportedApps:
        for app in self.supportedApps:
            APP_REGISTRY[app]['dpAddedMethod'](self)
    for appdef in implicitApps():
        appdef[2]['dpAddedMethod'](self)

    # Modify immediately addable types if necessary (keeping the order of
    # locally allowed types as the constrains form does).
    for gf in group_folders:
        gf.update_immediately_addable_types(allowed_before[gf])


@adapter(IDocumentPool, IObjectRemovedEvent)
def docPoolRemoved(obj, event=None):
    """
    """
    self = obj
    # Trigger my own method
    APP_REGISTRY[BASE_APP]['dpRemovedMethod'](self)
    # Trigger configs for all applications
    if self.supportedApps:
        for app in self.supportedApps:
            APP_REGISTRY[app]['dpRemovedMethod'](self)
    for appdef in implicitApps():
        appdef[2]['dpRemovedMethod'](self)
    notify(DocumentPoolRemovedEvent(self))
