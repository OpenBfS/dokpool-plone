# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from Acquisition import aq_inner
from docpool.elan.config import ELAN_APP
from docpool.transfers.behaviors.transferable import ITransferable
from elan.esd import DocpoolMessageFactory as _
from plone.autoform.directives import read_permission
from plone.autoform.interfaces import IFormFieldProvider
from plone.directives import form
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class IELANDocument(ITransferable):
    """
    """

    scenarios = schema.List(
        title=_(
            u'label_dpdocument_scenarios',
            default=u'Belongs to scenarios'),
        description=_(u'description_dpdocument_scenarios', default=u''),
        required=True,
        value_type=schema.Choice(source="docpool.event.vocabularies.Events"),
    )
    read_permission(scenarios='docpool.elan.AccessELAN')
    form.widget(scenarios=CheckBoxFieldWidget)


@form.default_value(field=IELANDocument['scenarios'])
def initializeScenarios(data):
    if hasattr(data.context, "getUserSelectedScenarios"):
        return data.context.getUserSelectedScenarios()
    else:
        return []


class ELANDocument(object):

    __allow_access_to_unprotected_subobjects__ = 1

    security = ClassSecurityInfo()

    def __init__(self, context):
        self.context = context

    def _get_scenarios(self):
        return self.context.doc_extension(ELAN_APP).scenarios

    def _set_scenarios(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.doc_extension(ELAN_APP).scenarios = value

    scenarios = property(_get_scenarios, _set_scenarios)
