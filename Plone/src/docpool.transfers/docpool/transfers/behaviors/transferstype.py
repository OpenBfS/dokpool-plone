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
from docpool.transfers.db.query import allowed_targets
from plone.autoform.directives import widget
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from Products.CMFPlone.utils import safe_unicode
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.interface import provider
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@provider(IContextSourceBinder)
def possible_targets_vocabulary_factory(context):
    targets = allowed_targets(context)
    return SimpleVocabulary([
        SimpleTerm(t.tf_uid, t.tf_uid, safe_unicode(t)) for t in targets])


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

    widget(automaticTransferTargets=CheckBoxFieldWidget)
    automaticTransferTargets = schema.List(
        title=_(
            u'label_doctype_automatictransfertargets',
            default=u'Where are documents of this type transferred automatically?',
        ),
        description=_(
            u'description_doctype_automatictransfertargets', default=u''),
        required=False,
        value_type=schema.Choice(
            title=_(u'Transfer target'),
            source=possible_targets_vocabulary_factory,
        ),
    )


class TransfersType(object):
    """
    """

    def __init__(self, context):
        self.context = context

    @property
    def allowTransfer(self):
        return getattr(self.context, "allowTransfer", True)

    @allowTransfer.setter
    def allowTransfer(self, value):
        context = aq_inner(self.context)
        context.allowTransfer = value

    @property
    def automaticTransferTargets(self):
        value = set(getattr(self.context, 'automaticTransferTargets', ()) or ())
        if not value:
            # avoid unnecessary interaction with the zope.sqlalchemy datamanager
            return []
        allowed = {target.tf_uid: target for target in allowed_targets(self.context)}
        return sorted(
            value.intersection(allowed),
            key=lambda tid: safe_unicode(allowed[tid])
        )

    @automaticTransferTargets.setter
    def automaticTransferTargets(self, value):
        try:
            self.context.myDocumentPool()
        except AttributeError:
            return

        context = aq_inner(self.context)
        unaffected = set(getattr(context, 'automaticTransferTargets', ()) or ())
        if unaffected:
            allowed = (target.tf_uid for target in allowed_targets(context))
            unaffected.difference_update(allowed)
        context.automaticTransferTargets = tuple(unaffected.union(value))
