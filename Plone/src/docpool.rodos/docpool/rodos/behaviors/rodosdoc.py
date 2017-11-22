# -*- coding: utf-8 -*-
"""Common configuration constants
"""
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


class RodosDoc(FlexibleView):
    __allow_access_to_unprotected_subobjects__ = 1

    security = ClassSecurityInfo()

    appname = Rodos_APP

    def __init__(self, context):
        self.context = context
        self.request = context.REQUEST
    
    def _get_rodos_reportId(self):
        return self.context.reportId

    def _set_rodos_reportId(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.reportId = value
    
    reportId = property(_get_rodos_reportId, _set_rodos_reportId)


    def isClean(self):
        """
        Is this document free for further action like publishing or transfer?
        @return:
        """
        # TODO: define if necessary. Method MUST be present in Doc behavior.
        return True
