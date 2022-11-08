from AccessControl import ClassSecurityInfo
from Acquisition import aq_inner
from docpool.base.behaviors.transferable import ITransferable
from docpool.elan.config import ELAN_APP
from docpool.elan.utils import getScenariosForCurrentUser
from elan.esd import DocpoolMessageFactory as _
from plone.autoform import directives
from plone.autoform.directives import read_permission
from plone.autoform.interfaces import IFormFieldProvider
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory


@provider(IContextAwareDefaultFactory)
def initializeScenarios(context):
    return getScenariosForCurrentUser()


@provider(IFormFieldProvider)
class IELANDocument(ITransferable):
    """ """

    scenarios = schema.List(
        title=_("label_dpdocument_scenarios", default="Belongs to scenarios"),
        description=_("description_dpdocument_scenarios", default=""),
        required=True,
        defaultFactory=initializeScenarios,
        value_type=schema.Choice(source="docpool.elan.vocabularies.Events"),
    )
    read_permission(scenarios="docpool.elan.AccessELAN")
    directives.widget(scenarios=CheckBoxFieldWidget)


class ELANDocument:

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
