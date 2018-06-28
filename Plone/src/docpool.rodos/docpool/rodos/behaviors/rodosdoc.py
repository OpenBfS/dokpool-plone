# -*- coding: utf-8 -*-
"""Common configuration constants
"""
from Products.Archetypes.utils import shasattr
from docpool.base.utils import getInheritedValue
from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform.directives import read_permission, write_permission
from plone.directives import form
from zope.interface import provider, implementer
from zope import schema
from docpool.base import DocpoolMessageFactory as _
from docpool.base.browser.flexible_view import FlexibleView
from docpool.rodos.config import Rodos_APP
from AccessControl import ClassSecurityInfo
from docpool.base.interfaces import IDocumentExtension
from collective import dexteritytextindexer
from Products.CMFPlone.utils import parent

from docpool.rodos import DocpoolMessageFactory as _

from Acquisition import aq_inner


@provider(IFormFieldProvider)
class IRodosDoc(IDocumentExtension):
    reportId = schema.TextLine(
                        title=_(u'label_rodos_reportId', default=u'Report ID'),
                        description=_(u'description_rodos_reportId', default=u''),
                        required=True,
    )
    read_permission(reportId='docpool.rodos.AccessRodos')
    write_permission(reportId='docpool.rodos.AccessRodos')
    dexteritytextindexer.searchable('reportId')

    releaseSite = schema.TextLine(
                        title=_(u'label_rodos_releaseSite', default=u'Release Site'),
                        description=_(u'description_rodos_releaseSite', default=u''),
                        required=False,
    )
    read_permission(releaseSite='docpool.rodos.AccessRodos')
    write_permission(releaseSite='docpool.rodos.AccessRodos')
    dexteritytextindexer.searchable('releaseSite')

    releaseStart = schema.Datetime(
                        title=_(u'label_rodos_releaseStart', default=u'Release Start'),
                        description=_(u'description_rodos_releaseStart', default=u''),
                        required=False,
    )
    read_permission(releaseStart='docpool.rodos.AccessRodos')
    write_permission(releaseStart='docpool.rodos.AccessRodos')


class RodosDoc(FlexibleView):
    __allow_access_to_unprotected_subobjects__ = 1

    security = ClassSecurityInfo()

    appname = Rodos_APP

    def __init__(self, context):
        self.context = context
        self.request = context.REQUEST
    
    def _get_rodos_reportId(self):
        return getInheritedValue(self, "reportId")

    def _set_rodos_reportId(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.reportId = value
    
    reportId = property(_get_rodos_reportId, _set_rodos_reportId)

    def _get_rodos_releaseSite(self):
        return getInheritedValue(self, "releaseSite")

    def _set_rodos_releaseSite(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.releaseSite = value

    releaseSite = property(_get_rodos_releaseSite, _set_rodos_releaseSite)

    def _get_rodos_releaseStart(self):
        return getInheritedValue(self, "releaseStart")

    def _set_rodos_releaseStart(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.releaseStart = value

    releaseStart = property(_get_rodos_releaseStart, _set_rodos_releaseStart)

    def isClean(self):
        """
        Is this document free for further action like publishing or transfer?
        @return:
        """
        # TODO: define if necessary. Method MUST be present in Doc behavior.
        return True