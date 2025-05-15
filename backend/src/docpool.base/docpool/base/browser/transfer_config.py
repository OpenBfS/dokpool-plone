from docpool.base import DocpoolMessageFactory as _
from docpool.base.behaviors.transferstype import ITransfersType
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
        value_type=schema.Choice(source="docpool.base.vocabularies.DocumentTypes"),
    )
    directives.widget(types=CheckBoxFieldWidget)

    targets = schema.List(
        title=_("label_transfer_config_transfer_targets", default="Transfer targets"),
        description=_(
            "desc_transfer_config_transfer_targets",
            default="Which automatic transfer targets to set or unset for the types selected above.",
        ),
        required=False,
        missing_value=(),
        value_type=schema.Choice(source="docpool.transfers.vocabularies.TransferTargets"),
    )
    directives.widget(targets=CheckBoxFieldWidget)


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

        doctypes = self.context["dtypes"]
        types = [doctypes[t] for t in data["types"]]
        targets = data["targets"]

        for doctype in types:
            ITransfersType(doctype).automaticTransferTargets = targets

        self.status = f"Configured {len(types)} types for {len(targets)} targets."
