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
from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile
from zope.interface import implementer
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import logging


logger = logging.getLogger(__name__)


class ITransferConfig(model.Schema):
    add = schema.Choice(
        title=_(
            "label_transfer_config_add_or_remove",
            default="Automatic transfer for selected document types:",
        ),
        required=True,
        default=True,
        source=SimpleVocabulary([
            SimpleTerm(True, title=_("label_transfer_config_add", default="add")),
            SimpleTerm(False, title=_("label_transfer_config_remove", default="remove")),
        ]),
    )
    directives.widget(add=RadioFieldWidget)

    types = schema.List(
        title=_("label_transfer_config_document_types", default="Document types"),
        description=_(
            "desc_transfer_config_document_types",
            default="Document types that shall be transferred from now on, or whose transferral shall be ended.",
        ),
        required=True,
        min_length=1,
        value_type=schema.Choice(source="docpool.base.vocabularies.DocType"),
    )
    directives.widget(
        "types",
        CheckBoxFieldWidget,
        template=ViewPageTemplateFile("templates/checklist_input.pt"),
    )

    targets = schema.List(
        title=_("label_transfer_config_transfer_targets", default="Transfer targets"),
        description=_(
            "desc_transfer_config_transfer_targets",
            default="Automatic transfer targets to add or remove for the document types selected above.",
        ),
        required=True,
        min_length=1,
        value_type=schema.Choice(source="docpool.transfers.vocabularies.TransferTargets"),
    )
    directives.widget(targets=CheckBoxFieldWidget)


@implementer(IDexterityEditForm)
@layout.wrap_form
class TransferConfigView(AutoExtensibleForm, form.Form):
    label = _("Transfer config")
    ignoreContext = True
    schema = ITransferConfig
    template = ViewPageTemplateFile("templates/transfer_config.pt")

    def update(self):
        self.portal_type = self.context.portal_type
        self.request.setupLocale()
        self.language = self.request._locale.id.language
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
        add = data["add"]

        for doctype in types:
            doctype_targets = set(ITransfersType(doctype).automaticTransferTargets)
            if add:
                doctype_targets.update(targets)
            else:
                doctype_targets.difference_update(targets)
            ITransfersType(doctype).automaticTransferTargets = list(doctype_targets)

        self.status = _(
            "status_transfer_config_success",
            default="Configured ${targets} target(s) for ${types} type(s).",
            mapping=dict(targets=len(targets), types=len(types)),
        )

    @button.buttonAndHandler(_("label_cancel", default="Cancel"), name="cancel")
    def handle_cancel(self, action):
        return self.request.response.redirect(self.context.myDocumentPool().absolute_url())
