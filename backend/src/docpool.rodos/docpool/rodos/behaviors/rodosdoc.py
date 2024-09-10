from docpool.base.browser.flexible_view import FlexibleView
from docpool.base.interfaces import IDocumentExtension
from docpool.rodos import DocpoolMessageFactory as _
from docpool.rodos.config import RODOS_APP
from plone.app.dexterity.textindexer.directives import searchable
from plone.autoform import directives
from plone.autoform.directives import read_permission
from plone.autoform.directives import write_permission
from plone.autoform.interfaces import IFormFieldProvider
from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class IRodosDoc(IDocumentExtension):
    PrognosisForm = schema.Choice(
        title=_("label_rodos_PrognosisForm", default="RODOS Typ"),
        description=_("description_rodos_PrognosisForm", default=""),
        source="docpool.rodos.vocabularies.PrognosisForms",
        required=False,
    )
    directives.widget(PrognosisForm=RadioFieldWidget)
    read_permission(PrognosisForm="docpool.rodos.AccessRodos")
    write_permission(PrognosisForm="docpool.rodos.AccessRodos")
    searchable("PrognosisForm")

    PrognosisType = schema.Choice(
        title=_("Prognosis Type"),
        description=_("description_rodos_PrognosisType", default=""),
        source="docpool.rodos.vocabularies.PrognosisTypes",
        required=False,
    )
    read_permission(PrognosisType="docpool.rodos.AccessRodos")
    write_permission(PrognosisType="docpool.rodos.AccessRodos")
    searchable("PrognosisType")


class RodosDoc(FlexibleView):
    appname = RODOS_APP

    def __init__(self, context):
        self.context = context
        self.request = context.REQUEST

    @property
    def PrognosisType(self):
        return self.context.PrognosisType

    @PrognosisType.setter
    def PrognosisType(self, value):
        self.context.PrognosisType = value

    @property
    def PrognosisForm(self):
        return self.context.PrognosisForm

    @PrognosisForm.setter
    def PrognosisForm(self, value):
        self.context.PrognosisForm = value

    def isClean(self):
        """
        Is this document free for further action like publishing or transfer?
        @return:
        """
        # TODO: define if necessary. Method MUST be present in Doc behavior.
        return True
