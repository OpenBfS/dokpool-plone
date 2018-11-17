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
from docpool.rei.config import REI_APP
from AccessControl import ClassSecurityInfo
from docpool.base.interfaces import IDocumentExtension
from collective import dexteritytextindexer
from Products.CMFPlone.utils import parent

from z3c.form.browser.radio import RadioFieldWidget

from docpool.rei import DocpoolMessageFactory as _

from Acquisition import aq_inner


@provider(IFormFieldProvider)
class IREIDoc(IDocumentExtension):
    pass


class REIDoc(FlexibleView):
    __allow_access_to_unprotected_subobjects__ = 1

    security = ClassSecurityInfo()

    appname = REI_APP

    def __init__(self, context):
        self.context = context
        self.request = context.REQUEST



    def isClean(self):
        """
        Is this document free for further action like publishing or transfer?
        @return:
        """
        # TODO: define if necessary. Method MUST be present in Doc behavior.
        return True
