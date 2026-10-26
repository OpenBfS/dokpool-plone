from Acquisition import aq_inner
from docpool.base import DocpoolMessageFactory as _
from docpool.base.content.dptransferfolder import target_transfer_folders_for_docpool
from docpool.base.content.places import IPlaces
from plone.autoform.directives import widget
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.interface import provider


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
            source="docpool.transfers.vocabularies.AllowedTransferTargets",
        ),
    )


class TransferRelatedMixin:
    def assert_target_allowed(self, target):
        pass

    def allowed_targets(self):
        targets = target_transfer_folders_for_docpool(self.context)
        for target in targets[:]:
            try:
                self.assert_target_allowed(target)
            except BaseException:
                targets.remove(target)
        return targets


class TransfersType(TransferRelatedMixin):
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
        return value.intersection(target.UID() for target in self.allowed_targets())

    @automaticTransferTargets.setter
    def automaticTransferTargets(self, value):
        if IPlaces(self.context).document_pool is None:
            return

        context = aq_inner(self.context)
        unaffected = set(getattr(context, "automaticTransferTargets", ()) or ())
        if unaffected:
            unaffected.difference_update(target.UID() for target in self.allowed_targets())
        context.automaticTransferTargets = tuple(unaffected.union(value))

    def assert_target_allowed(self, target):
        """
        Other ESD must have allowed communication with my ESD (Transfer folder exists)
        and either my DocType is known and must be accepted
            or the DocType is not defined in the other ESD (or don't exist because e.g., we're creating it)
               and default is not to block.
        """
        if not target.acceptsDT(self.context.id):
            raise ValueError(_("Doc type not accepted."))
