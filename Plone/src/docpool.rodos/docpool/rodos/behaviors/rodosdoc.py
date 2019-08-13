# -*- coding: utf-8 -*-
"""Common configuration constants
"""
from AccessControl import ClassSecurityInfo
from Acquisition import aq_inner
from collective import dexteritytextindexer
from docpool.base import DocpoolMessageFactory as _
from docpool.base.browser.flexible_view import FlexibleView
from docpool.base.interfaces import IDocumentExtension
from docpool.base.utils import getInheritedValue
from docpool.rodos import DocpoolMessageFactory as _
from docpool.rodos.config import Rodos_APP
from plone.autoform import directives
from plone.autoform.directives import read_permission
from plone.autoform.directives import write_permission
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.form.browser.radio import RadioFieldWidget
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class IRodosDoc(IDocumentExtension):
    ReportId = schema.TextLine(
        title=_(u'label_rodos_ReportId', default=u'Report ID'),
        description=_(u'description_rodos_ReportId', default=u''),
        required=False,
    )
    read_permission(ReportId='docpool.rodos.AccessRodos')
    write_permission(ReportId='docpool.rodos.AccessRodos')
    dexteritytextindexer.searchable('ReportId')

    CalculationDate = schema.Datetime(
        title=_(u'label_rodos_CalculationDate', default=u'Calculation Date'),
        description=_(u'description_rodos_CalculationDate', default=u''),
        required=True,
    )
    read_permission(CalculationDate='docpool.rodos.AccessRodos')
    write_permission(CalculationDate='docpool.rodos.AccessRodos')

    ProjectUser = schema.TextLine(
        title=_(u'label_rodos_ProjectUser', default=u'Project User'),
        description=_(u'description_rodos_ProjectUser', default=u''),
        required=False,
    )
    read_permission(ProjectUser='docpool.rodos.AccessRodos')
    write_permission(ProjectUser='docpool.rodos.AccessRodos')
    dexteritytextindexer.searchable('ProjectUser')

    ProjectName = schema.TextLine(
        title=_(u'label_rodos_ProjectName', default=u'Project Name'),
        description=_(u'description_rodos_ProjectName', default=u''),
        required=True,
    )
    read_permission(ProjectName='docpool.rodos.AccessRodos')
    write_permission(ProjectName='docpool.rodos.AccessRodos')
    dexteritytextindexer.searchable('ProjectName')

    PrognosisForm = schema.Choice(
        title=_(u'label_rodos_PrognosisForm', default=u'Prognosis Form'),
        description=_(u'description_rodos_PrognosisForm', default=u''),
        source="docpool.rodos.vocabularies.PrognosisForms",
        required=True,
    )
    directives.widget(PrognosisForm=RadioFieldWidget)
    read_permission(PrognosisForm='docpool.rodos.AccessRodos')
    write_permission(PrognosisForm='docpool.rodos.AccessRodos')
    dexteritytextindexer.searchable('PrognosisForm')

    ReleaseSite = schema.Choice(
        title=_(u'label_rodos_ReleaseSite', default=u'Release Site'),
        description=_(u'description_rodos_ReleaseSite', default=u''),
        source="docpool.rodos.vocabularies.ReleaseSites",
        required=False,
    )
    read_permission(ReleaseSite='docpool.rodos.AccessRodos')
    write_permission(ReleaseSite='docpool.rodos.AccessRodos')
    dexteritytextindexer.searchable('ReleaseSite')

    ReleaseStart = schema.Datetime(
        title=_(u'label_rodos_ReleaseStart', default=u'Release Start'),
        description=_(u'description_rodos_ReleaseStart', default=u''),
        required=False,
    )
    read_permission(ReleaseStart='docpool.rodos.AccessRodos')
    write_permission(ReleaseStart='docpool.rodos.AccessRodos')

    ReleaseStop = schema.Datetime(
        title=_(u'label_rodos_ReleaseStop', default=u'Release Stop'),
        description=_(u'description_rodos_ReleaseStop', default=u''),
        required=False,
    )
    read_permission(ReleaseStop='docpool.rodos.AccessRodos')
    write_permission(ReleaseStop='docpool.rodos.AccessRodos')

    PrognosisType = schema.Choice(
        title=_(u"Prognosis Type"),
        description=_(u'description_rodos_PrognosisType', default=u''),
        source="docpool.rodos.vocabularies.PrognosisTypes",
        required=False,
    )

    read_permission(PrognosisType='docpool.rodos.AccessRodos')
    write_permission(PrognosisType='docpool.rodos.AccessRodos')
    dexteritytextindexer.searchable('PrognosisType')

    Model = schema.TextLine(
        title=_(u'label_rodos_Model', default=u'Model'),
        description=_(u'description_rodos_Model', default=u''),
        required=False,
    )
    read_permission(Model='docpool.rodos.AccessRodos')
    write_permission(Model='docpool.rodos.AccessRodos')
    dexteritytextindexer.searchable('Model')

    PrognosisBegin = schema.Datetime(
        title=_(u'label_rodos_PrognosisBegin', default=u'Prognosis Begin'),
        description=_(u'description_rodos_PrognosisBegin', default=u''),
        required=False,
    )
    read_permission(PrognosisBegin='docpool.rodos.AccessRodos')
    write_permission(PrognosisBegin='docpool.rodos.AccessRodos')

    PrognosisEnd = schema.Datetime(
        title=_(u'label_rodos_PrognosisEnd', default=u'Prognosis End'),
        description=_(u'description_rodos_PrognosisEnd', default=u''),
        required=False,
    )
    read_permission(PrognosisEnd='docpool.rodos.AccessRodos')
    write_permission(PrognosisEnd='docpool.rodos.AccessRodos')

    NumericWeatherPredictionDate = schema.TextLine(
        title=_(
            u'label_rodos_NumericWeatherPredictionDate',
            default=u'Numeric Weather Prediction Date',
        ),
        description=_(
            u'description_rodos_NumericWeatherPredictionDate',
            default=u''),
        required=False,
    )
    read_permission(NumericWeatherPredictionDate='docpool.rodos.AccessRodos')
    write_permission(NumericWeatherPredictionDate='docpool.rodos.AccessRodos')
    dexteritytextindexer.searchable('NumericWeatherPredictionDate')


class RodosDoc(FlexibleView):
    __allow_access_to_unprotected_subobjects__ = 1

    security = ClassSecurityInfo()

    appname = Rodos_APP

    def __init__(self, context):
        self.context = context
        self.request = context.REQUEST

    def _get_rodos_ProjectName(self):
        return getInheritedValue(self, "ProjectName")

    def _set_rodos_ProjectName(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.ProjectName = value

    ProjectName = property(_get_rodos_ProjectName, _set_rodos_ProjectName)

    def _get_rodos_ReportId(self):
        return getInheritedValue(self, "ReportId")

    def _set_rodos_ReportId(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.ReportId = value

    ReportId = property(_get_rodos_ReportId, _set_rodos_ReportId)

    def _get_rodos_ReleaseSite(self):
        return getInheritedValue(self, "ReleaseSite")

    def _set_rodos_ReleaseSite(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.ReleaseSite = value

    ReleaseSite = property(_get_rodos_ReleaseSite, _set_rodos_ReleaseSite)

    def _get_rodos_ReleaseStart(self):
        return getInheritedValue(self, "ReleaseStart")

    def _set_rodos_ReleaseStart(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.ReleaseStart = value

    ReleaseStart = property(_get_rodos_ReleaseStart, _set_rodos_ReleaseStart)

    def _get_rodos_ReleaseStop(self):
        return getInheritedValue(self, "ReleaseStop")

    def _set_rodos_ReleaseStop(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.ReleaseStop = value

    ReleaseStop = property(_get_rodos_ReleaseStop, _set_rodos_ReleaseStop)

    def _get_rodos_PrognosisBegin(self):
        return getInheritedValue(self, "PrognosisBegin")

    def _set_rodos_PrognosisBegin(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.PrognosisBegin = value

    PrognosisBegin = property(
        _get_rodos_PrognosisBegin,
        _set_rodos_PrognosisBegin)

    def _get_rodos_PrognosisEnd(self):
        return getInheritedValue(self, "PrognosisEnd")

    def _set_rodos_PrognosisEnd(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.PrognosisEnd = value

    PrognosisEnd = property(_get_rodos_PrognosisEnd, _set_rodos_PrognosisEnd)

    def _get_rodos_NumericWeatherPredictionDate(self):
        return getInheritedValue(self, "NumericWeatherPredictionDate")

    def _set_rodos_NumericWeatherPredictionDate(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.NumericWeatherPredictionDate = value

    NumericWeatherPredictionDate = property(
        _get_rodos_NumericWeatherPredictionDate, _set_rodos_NumericWeatherPredictionDate
    )

    def _get_rodos_Model(self):
        return getInheritedValue(self, "Model")

    def _set_rodos_Model(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.Model = value

    Model = property(_get_rodos_Model, _set_rodos_Model)

    def _get_rodos_CalculationDate(self):
        return getInheritedValue(self, "CalculationDate")

    def _set_rodos_CalculationDate(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.CalculationDate = value

    CalculationDate = property(
        _get_rodos_CalculationDate,
        _set_rodos_CalculationDate)

    def _get_rodos_ProjectUser(self):
        return getInheritedValue(self, "ProjectUser")

    def _set_rodos_ProjectUser(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.ProjectUser = value

    ProjectUser = property(_get_rodos_ProjectUser, _set_rodos_ProjectUser)

    def _get_rodos_PrognosisType(self):
        return getInheritedValue(self, "PrognosisType")

    def _set_rodos_PrognosisType(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.PrognosisType = value

    PrognosisType = property(
        _get_rodos_PrognosisType,
        _set_rodos_PrognosisType)

    def _get_rodos_PrognosisForm(self):
        return getInheritedValue(self, "PrognosisForm")

    def _set_rodos_PrognosisForm(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.PrognosisForm = value

    PrognosisForm = property(
        _get_rodos_PrognosisForm,
        _set_rodos_PrognosisForm)

    def isClean(self):
        """
        Is this document free for further action like publishing or transfer?
        @return:
        """
        # TODO: define if necessary. Method MUST be present in Doc behavior.
        return True
