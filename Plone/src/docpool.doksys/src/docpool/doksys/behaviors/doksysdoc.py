# -*- coding: utf-8 -*-
"""Common configuration constants
"""
from collective import dexteritytextindexer
from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform.directives import read_permission, write_permission
from plone.directives import form
from zope.interface import provider, implementer
from zope import schema
from docpool.base import DocpoolMessageFactory as _
from docpool.base.browser.flexible_view import FlexibleView
from docpool.doksys.config import DOKSYS_APP
from AccessControl import ClassSecurityInfo
from docpool.base.interfaces import IDocumentExtension

from docpool.doksys import DocpoolMessageFactory as _

from Acquisition import aq_inner


@provider(IFormFieldProvider)
class IDoksysDoc(IDocumentExtension):
    #dexteritytextindexer.searchable('network_operator') # if a field is supposed to be fulltext searchable

    network_operator = schema.TextLine(
                        title=_(u'label_doksys_network_operator', default=u'Network Operator'),
                        description=_(u'description_doksys_network_operator', default=u''),
                        required=False,
    )
    read_permission(network_operator='docpool.doksys.AccessDoksys')
    write_permission(network_operator='docpool.doksys.AccessDoksys')


class DoksysDoc(FlexibleView):
    __allow_access_to_unprotected_subobjects__ = 1

    security = ClassSecurityInfo()

    appname = DOKSYS_APP

    def __init__(self, context):
        self.context = context
        self.request = context.REQUEST
    
    def _get_network_operator(self):
        return self.context.network_operator

    def _set_network_operator(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.network_operator = value

    network_operator = property(_get_network_operator, _set_network_operator)


    def isClean(self):
        """
        Is this document free for further action like publishing or transfer?
        @return:
        """
        # TODO: define if necessary. Method MUST be present in Doc behavior.
        return True
