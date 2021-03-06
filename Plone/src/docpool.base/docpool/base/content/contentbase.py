# -*- coding: utf-8 -*-
#
# File: contentbase.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the ContentBase content type. See contentbase.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from Acquisition import aq_base
from Acquisition import aq_inner
from Acquisition import aq_parent
from docpool.base import DocpoolMessageFactory as _
from plone import api
from plone.dexterity.content import Item
from plone.dexterity.interfaces import IEditFinishedEvent
from plone.supermodel import model
from plone.autoform import directives
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import base_hasattr
from Products.CMFPlone.utils import safe_unicode
from Products.DCWorkflow.interfaces import IAfterTransitionEvent
from zope import schema
from zope.component import adapter
from zope.interface import implementer
from zope.interface import provider
from zope.lifecycleevent import IObjectAddedEvent
from zope.lifecycleevent.interfaces import IObjectCopiedEvent
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from zope.schema.interfaces import IContextAwareDefaultFactory

import datetime


@provider(IContextAwareDefaultFactory)
def initializeMdate(context):
    return (
        context.created().asdatetime().replace(tzinfo=None)
        or datetime.datetime.now()
    )


class IContentBase(model.Schema):
    """
    """

    created_by = schema.TextLine(
        title=_(u'label_contentbase_created_by', default=u'Created by'),
        description=_(u'description_contentbase_created_by', default=u''),
        required=False,
    )
    directives.omitted('created_by')

    modified_by = schema.TextLine(
        title=_(u'label_contentbase_modified_by', default=u'Modified by'),
        description=_(u'description_contentbase_modified_by', default=u''),
        required=False,
    )
    directives.omitted('modified_by')

    mdate = schema.Datetime(
        title=_(u'label_contentbase_mdate',
                default=u'Date of last user action'),
        description=_(u'description_contentbase_mdate', default=u''),
        required=False,
        defaultFactory=initializeMdate,
    )
    directives.omitted('mdate')

    wdate = schema.Datetime(
        title=_(u'label_contentbase_wdate',
                default=u'Date of last workflow action'),
        description=_(u'description_contentbase_wdate', default=u''),
        required=False,
    )
    directives.omitted('wdate')


@implementer(IContentBase)
class ContentBase(Item):
    """
    """

    security = ClassSecurityInfo()

    def _getUserInfoString(self, plain=False):
        from docpool.base.utils import getUserInfo

        userid, fullname, primary_group = getUserInfo(self)
        # print userid, fullname, primary_group
        res = safe_unicode(fullname)
        if primary_group:
            if plain:
                res += u" %s" % safe_unicode(primary_group)
            else:
                res += u" <i>%s</i>" % safe_unicode(primary_group)
        return res

    def getWdate(self):
        """
        """
        return self.wdate

    def update_created(self):
        """
        """
        self.created_by = self._getUserInfoString()

    def getMdate(self):
        """
        """
        return (
            base_hasattr(self, "mdate") and self.mdate
        ) or self.created().asdatetime().replace(tzinfo=None)

    def changed(self):
        """
        """
        return self.getMdate()

    def update_modified(self):
        """
        """
        # print "update_modified"
        self.modified_by = self._getUserInfoString()
        self.mdate = datetime.datetime.now()
        self.reindexObject()

    def update_workflow(self):
        self.wdate = datetime.datetime.now()
        self.reindexObject()

    def modInfo(self, show_created=False):
        """
        """
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
        return (
            "Groups" in self.getPhysicalPath() or "Transfers" in self.getPhysicalPath()
        )

    def myGroup(self):
        """
        """
        pp = self.getPhysicalPath()
        if "Groups" in pp:
            i = pp.index("Groups")
            return self.restrictedTraverse("/".join(pp[: i + 2])).title
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
        wtool = getToolByName(self, 'portal_workflow')
        # wtool.updateRoleMappings(context)    # passing context is not possible :(
        #
        # Since WorkflowTool.updateRoleMappings()  from the line above supports
        # only sitewide updates code from updateRoleMappings() was copied below
        # to enable context passing to wftool._recursiveUpdateRoleMappings()
        wfs = {}
        for id in wtool.objectIds():
            wf = wtool.getWorkflowById(id)
            if hasattr(aq_base(wf), 'updateRoleMappingsFor'):
                wfs[id] = wf
        context = aq_parent(aq_inner(self))
        wtool._recursiveUpdateRoleMappings(context, wfs)


@adapter(IContentBase, IObjectAddedEvent)
def updateCreated(obj, event=None):
    request = obj.REQUEST
    if request.get('creating', False):
        # print "#" * 20, "creating"
        if not obj.isArchive():
            obj.update_created()
        obj.createActions()


# edited
@adapter(IContentBase, IEditFinishedEvent)
# Edit was finished and contents are saved. This event is fired
#    even when no changes happen (and no modified event is fired.)
def updateModified(obj, event=None):
    if not obj.isArchive():
        obj.update_modified()


@adapter(IContentBase, IObjectCreatedEvent)
def markCreateEvent(obj, event):
    if IObjectCopiedEvent.providedBy(event):
        return
    context = api.portal.get()
    request = context.REQUEST
    request.set("creating", True)


@adapter(IContentBase, IAfterTransitionEvent)
# Edit was finished and contents are saved. This event is fired
#    even when no changes happen (and no modified event is fired.)
def updateWorkflow(obj, event=None):
    if not obj.isArchive():
        obj.update_workflow()
