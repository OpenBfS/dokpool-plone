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
from Acquisition import aq_inner
from docpool.transfers import DocpoolMessageFactory as _
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class ITransfersType(model.Schema):
    allowTransfer = schema.Bool(
        title=_(
            u'label_doctype_allowtransfer',
            default=u'Can documents of this type be sent to other ESDs?',
        ),
        description=_(u'description_doctype_allowtransfer', default=u''),
        required=False,
        default=True,
    )


class TransfersType(object):
    """
    """

    def __init__(self, context):
        self.context = context

    def _get_allowTransfer(self):
        return getattr(self.context, "allowTransfer", True)

    def _set_allowTransfer(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.allowTransfer = value

    allowTransfer = property(_get_allowTransfer, _set_allowTransfer)
