# -*- coding: utf-8 -*-
#
# File: transferstype.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the TransfersType content type. See transferstype.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from zope.interface import implements
from zope.component import adapts
from zope import schema
from plone.autoform.interfaces import IFormFieldProvider
from zope.interface import provider, implementer
from plone.directives import form


from plone.dexterity.content import Item
from docpool.base.interfaces import IDocTypeExtension

from Products.CMFCore.utils import getToolByName

##code-section imports
from Acquisition import aq_inner
from docpool.transfers.config import TRANSFERS_APP
##/code-section imports

from docpool.transfers.config import PROJECTNAME

from docpool.transfers import DocpoolMessageFactory as _

@provider(IFormFieldProvider)
class ITransfersType(form.Schema):
    allowTransfer = schema.Bool(
        title=_(u'label_doctype_allowtransfer', default=u'Can documents of this type be sent to other ESDs?'),
        description=_(u'description_doctype_allowtransfer', default=u''),
        required=False,
        default=True,
    )


##/code-section interface


class TransfersType(object):
    """
    """

    def __init__(self, context):
        self.context = context
##code-section methods

    def _get_allowTransfer(self):
        return getattr(self.context, "allowTransfer", True)


    def _set_allowTransfer(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.allowTransfer = value


    allowTransfer = property(_get_allowTransfer, _set_allowTransfer)
##/code-section methods


##code-section bottom
##/code-section bottom 
