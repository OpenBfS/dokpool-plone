# -*- coding: utf-8 -*-
"""Common configuration constants
"""

from plone.autoform.interfaces import IFormFieldProvider
from plone.directives import form
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice, RelationList
from zope.interface import provider, implementer
from zope.component import adapter
from zope import schema
from docpool.base import DocpoolMessageFactory as _
from docpool.transfers.config import TRANSFERS_APP
from elan.esd.content.elandoccollection import IELANDocCollection
from five import grok
from plone.indexer.interfaces import IIndexer
from Products.ZCatalog.interfaces import IZCatalog
from Products.CMFCore.utils import getToolByName
from AccessControl import ClassSecurityInfo

from elan.dbaccess.dbinit import __session__
from elan.esd.db.model import Channel, DocTypePermission, SenderLog, ReceiverLog,\
    ChannelSends, ChannelReceives, ChannelPermissions
from sqlalchemy import and_
from datetime import datetime
from DateTime import DateTime
from elan.esd.content.transfers import determineTransferFolderObject,\
    ensureDocTypeInTarget, ensureScenariosInTarget, determineChannels
from sqlalchemy.sql.expression import desc, or_
from docpool.base.utils import execute_under_special_role,\
    _copyPaste, getUserInfo, portalMessage

from plone import api
from Products.CMFPlone.utils import log, log_exc
from elan.esd import DocpoolMessageFactory as _
from zope.lifecycleevent.interfaces import IObjectRemovedEvent

from Acquisition import aq_inner
from Products.Archetypes.utils import shasattr

class ITransferable(model.Schema):
    
    transferred_by = schema.TextLine(
                        title=_(u'label_dpdocument_transferred_by', default=u'Transferred by'),
                        description=_(u'description_dpdocument_transferred_by', default=u''),
                        required=False,
##code-section field_transferred_by
##/code-section field_transferred_by                           
    )
    form.omitted('transferred_by')
        
    transferred = schema.Datetime(
                        title=_(u'label_dpdocument_transferred', default=u'Date of last transfer'),
                        description=_(u'description_dpdocument_transferred', default=u''),
                        required=False,
##code-section field_transferred
##/code-section field_transferred                           
    )
    form.omitted('transferred')
        
    transferLog = schema.Text(
                        title=_(u'label_dpdocument_transferlog', default=u'Transfer log'),
                        description=_(u'description_dpdocument_transferlog', default=u'Only used for archived documents.'),
                        required=False,
##code-section field_transferLog
##/code-section field_transferLog                           
    )
    form.omitted('transferLog')


class Transferable(object):

    security = ClassSecurityInfo()

    def __init__(self, context):
        self.context = context
    
    def _get_transferred_by(self):
        return self.context.doc_extension(TRANSFERS_APP).transferred_by

    def _set_transferred_by(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.doc_extension(TRANSFERS_APP).transferred_by = value
    
    transferred_by = property(_get_transferred_by, _set_transferred_by)

    def _get_transferred(self):
        return self.context.doc_extension(TRANSFERS_APP).transferred

    def _set_transferred(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.doc_extension(TRANSFERS_APP).transferred = value
    
    transferred = property(_get_transferred, _set_transferred)

    def _get_transferLog(self):
        return self.context.doc_extension(TRANSFERS_APP).transferLog

    def _set_transferLog(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.doc_extension(TRANSFERS_APP).transferLog = value
    
    transferLog = property(_get_transferLog, _set_transferLog)

