from docpool.base import DocpoolMessageFactory as _
from docpool.base.behaviors.transferstype import ITransfersType
from plone import api
from plone.autoform import directives
from plone.autoform.form import AutoExtensibleForm
from plone.dexterity.interfaces import IDexterityEditForm
from plone.supermodel import model
from plone.z3cform import layout
from z3c.form import button
from z3c.form import form
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.interface import implementer

import logging


logger = logging.getLogger(__name__)


class ITransferConfig(model.Schema):
    types = schema.List(
        title=_("label_transfer_config_document_types", default="Document types"),
        description=_(
            "desc_transfer_config_document_types",
            default="Which document types to configure.",
        ),
        required=True,
        min_length=1,
        value_type=schema.Choice(source="docpool.base.vocabularies.DocType"),
    )
    directives.widget(types=CheckBoxFieldWidget)

    targets = schema.List(
        title=_("label_transfer_config_transfer_targets", default="Transfer targets"),
        description=_(
            "desc_transfer_config_transfer_targets",
            default="Which automatic transfer targets to set or unset for the types selected above.",
        ),
        required=True,
        min_length=1,
        value_type=schema.Choice(source="docpool.transfers.vocabularies.TransferTargets"),
    )
    directives.widget(targets=CheckBoxFieldWidget)

    remove = schema.Bool(
        title=_("label_transfer_config_remove", default="Remove selected targets?"),
        description=_(
            "desc_transfer_config_remove",
            default="Whether to remove the selected targets for the selected types. Default is to add them.",
        ),
        required=False,
        default=False,
    )


@implementer(IDexterityEditForm)
@layout.wrap_form
class TransferConfigView(AutoExtensibleForm, form.Form):
    label = _("Transfer config")
    ignoreContext = True
    schema = ITransferConfig

    def update(self):
        self.portal_type = self.context.portal_type
        super().update()

    def updateActions(self):
        super().updateActions()
        self.actions["apply"].addClass("btn-primary")

    @button.buttonAndHandler(_("Apply"), name="apply")
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        logger.info(str(data))

        types = [api.content.get(UID=t) for t in data["types"]]
        targets = data["targets"]
        remove = data["remove"]

        for doctype in types:
            doctype_targets = set(ITransfersType(doctype).automaticTransferTargets)
            if remove:
                doctype_targets.difference_update(targets)
            else:
                doctype_targets.update(targets)
            ITransfersType(doctype).automaticTransferTargets = list(doctype_targets)

        self.status = f"Configured {len(types)} types for {len(targets)} targets."
