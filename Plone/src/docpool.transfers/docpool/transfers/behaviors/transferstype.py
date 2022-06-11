#
# File: transferstype.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ""
__docformat__ = "plaintext"

"""Definition of the TransfersType content type. See transferstype.py for more
explanation on the statements below.
"""
from Acquisition import aq_inner
from docpool.transfers import DocpoolMessageFactory as _
from docpool.transfers.db.query import allowed_targets
from plone import api
from plone.autoform.directives import widget
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.interface import provider
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary


@provider(IContextSourceBinder)
def possible_targets_vocabulary_factory(context):
    targets = allowed_targets(context)
    target_title = lambda target: api.content.get(UID=target).from_to_title()
    return SimpleVocabulary([SimpleTerm(t, t, target_title(t)) for t in targets])


@provider(IFormFieldProvider)
class ITransfersType(model.Schema):
    allowTransfer = schema.Bool(
        title=_(
            "label_doctype_allowtransfer",
            default="Can documents of this type be sent to other ESDs?",
        ),
        description=_("description_doctype_allowtransfer", default=""),
        required=False,
        default=True,
    )

    widget(automaticTransferTargets=CheckBoxFieldWidget)
    automaticTransferTargets = schema.List(
        title=_(
            "label_doctype_automatictransfertargets",
            default="Where are documents of this type transferred automatically?",
        ),
        description=_("description_doctype_automatictransfertargets", default=""),
        required=False,
        value_type=schema.Choice(
            title=_("Transfer target"),
            source=possible_targets_vocabulary_factory,
        ),
    )


class TransfersType:
    """ """

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
        value = set(getattr(self.context, "automaticTransferTargets", ()) or ())
        if not value:
            # avoid unnecessary interaction with the zope.sqlalchemy datamanager
            return []
        allowed = {target for target in allowed_targets(self.context)}
        return sorted(
            value.intersection(allowed),
            key=lambda target: api.content.get(UID=target).from_to_title(),
        )

    @automaticTransferTargets.setter
    def automaticTransferTargets(self, value):
        try:
            self.context.myDocumentPool()
        except AttributeError:
            return

        context = aq_inner(self.context)
        unaffected = set(getattr(context, "automaticTransferTargets", ()) or ())
        if unaffected:
            allowed = (target for target in allowed_targets(context))
            unaffected.difference_update(allowed)
        context.automaticTransferTargets = tuple(unaffected.union(value))
