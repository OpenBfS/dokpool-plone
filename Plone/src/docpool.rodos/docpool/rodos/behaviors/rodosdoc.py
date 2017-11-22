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
from docpool.rodos.config import RODOS_APP
from AccessControl import ClassSecurityInfo
from docpool.base.interfaces import IDocumentExtension

from docpool.rodos import DocpoolMessageFactory as _

from Acquisition import aq_inner


@provider(IFormFieldProvider)
class IRodosDoc(IDocumentExtension):
    rodos_attribute = schema.TextLine(
                        title=_(u'label_rodos_attribute', default=u'Rodos Attribute'),
                        description=_(u'description_rodos_attribute', default=u''),
                        required=False,
    )
    read_permission(rodos_attribute='docpool.rodos.AccessRodos')
    write_permission(rodos_attribute='docpool.rodos.AccessRodos')


class RodosDoc(FlexibleView):
    __allow_access_to_unprotected_subobjects__ = 1

    security = ClassSecurityInfo()

    appname = RODOS_APP

    def __init__(self, context):
        self.context = context
        self.request = context.REQUEST
    
    def _get_rodos_attribute(self):
        return self.context.rodos_attribute

    def _set_rodos_attribute(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.rodos_attribute = value
    
    rodos_attribute = property(_get_rodos_attribute, _set_rodos_attribute)


    def isClean(self):
        """
        Is this document free for further action like publishing or transfer?
        @return:
        """
        # TODO: define if necessary. Method MUST be present in Doc behavior.
        return True
