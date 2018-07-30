# -*- coding: utf-8 -*-
"""Common configuration constants
"""
from Products.Archetypes.utils import shasattr
from docpool.base.utils import getInheritedValue
from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform.directives import read_permission, write_permission
from plone.directives import form
from zope.interface import provider, implementer
from zope import schema
from docpool.base import DocpoolMessageFactory as _
from docpool.base.browser.flexible_view import FlexibleView
from docpool.rodos.config import Rodos_APP
from AccessControl import ClassSecurityInfo
from docpool.base.interfaces import IDocumentExtension
from collective import dexteritytextindexer
from Products.CMFPlone.utils import parent

from z3c.form.browser.radio import RadioFieldWidget

from docpool.rodos import DocpoolMessageFactory as _

from Acquisition import aq_inner


@provider(IFormFieldProvider)
class IRodosDoc(IDocumentExtension):
    reportId = schema.TextLine(
                        title=_(u'label_rodos_reportId', default=u'Report ID'),
                        description=_(u'description_rodos_reportId', default=u''),
                        required=False,
    )
    read_permission(reportId='docpool.rodos.AccessRodos')
    write_permission(reportId='docpool.rodos.AccessRodos')
    dexteritytextindexer.searchable('reportId')


    calculationDate = schema.Datetime(
                        title=_(u'label_rodos_calculationDate', default=u'Calculation Date'),
                        description=_(u'description_rodos_calculationDate', default=u''),
                        required=True,
    )
    read_permission(calculationDate='docpool.rodos.AccessRodos')
    write_permission(calculationDate='docpool.rodos.AccessRodos')


    projectUser = schema.TextLine(
                        title=_(u'label_rodos_projectUser', default=u'Project User'),
                        description=_(u'description_rodos_projectUser', default=u''),
                        required=False,
    )
    read_permission(projectUser='docpool.rodos.AccessRodos')
    write_permission(projectUser='docpool.rodos.AccessRodos')
    dexteritytextindexer.searchable('projectUser')


    projectName = schema.TextLine(
                        title=_(u'label_rodos_projectName', default=u'Project Name'),
                        description=_(u'description_rodos_projectName', default=u''),
                        required=True,
    )
    read_permission(projectName='docpool.rodos.AccessRodos')
    write_permission(projectName='docpool.rodos.AccessRodos')
    dexteritytextindexer.searchable('projectName')


    prognosisForm = schema.Choice(
                        title=_(u'label_rodos_prognosisForm', default=u'Prognosis Form'),
                        description=_(u'description_rodos_prognosisForm', default=u''),
                        source="docpool.rodos.vocabularies.PrognosisForms",
                        required=True,
    )
    form.widget(prognosisForm=RadioFieldWidget)
    read_permission(prognosisForm='docpool.rodos.AccessRodos')
    write_permission(prognosisForm='docpool.rodos.AccessRodos')
    dexteritytextindexer.searchable('prognosisForm')


    releaseSite = schema.Choice(
                        title=_(u'label_rodos_releaseSite', default=u'Release Site'),
                        description=_(u'description_rodos_releaseSite', default=u''),
                        source="docpool.rodos.vocabularies.ReleaseSites",

                        required=False,
    )
    read_permission(releaseSite='docpool.rodos.AccessRodos')
    write_permission(releaseSite='docpool.rodos.AccessRodos')
    dexteritytextindexer.searchable('releaseSite')

    releaseStart = schema.Datetime(
                        title=_(u'label_rodos_releaseStart', default=u'Release Start'),
                        description=_(u'description_rodos_releaseStart', default=u''),
                        required=False,
    )
    read_permission(releaseStart='docpool.rodos.AccessRodos')
    write_permission(releaseStart='docpool.rodos.AccessRodos')

    releaseStop = schema.Datetime(
                        title=_(u'label_rodos_releaseStop', default=u'Release Stop'),
                        description=_(u'description_rodos_releaseStop', default=u''),
                        required=False,
    )
    read_permission(releaseStop='docpool.rodos.AccessRodos')
    write_permission(releaseStop='docpool.rodos.AccessRodos')


    prognosisType = schema.Choice(
            title=_(u"Prognosis Type"),
            description=_(u'description_rodos_prognosisType', default=u''),
            source="docpool.rodos.vocabularies.PrognosisTypes",
            required=False,
        )

    read_permission(prognosisType='docpool.rodos.AccessRodos')
    write_permission(prognosisType='docpool.rodos.AccessRodos')
    dexteritytextindexer.searchable('prognosisType')

    model = schema.TextLine(
                        title=_(u'label_rodos_model', default=u'Model'),
                        description=_(u'description_rodos_model', default=u''),
                        required=False,
    )
    read_permission(model='docpool.rodos.AccessRodos')
    write_permission(model='docpool.rodos.AccessRodos')
    dexteritytextindexer.searchable('model')


    prognosisBegin = schema.Datetime(
                        title=_(u'label_rodos_prognosisBegin', default=u'Prognosis Begin'),
                        description=_(u'description_rodos_prognosisBegin', default=u''),
                        required=False,
    )
    read_permission(prognosisBegin='docpool.rodos.AccessRodos')
    write_permission(prognosisBegin='docpool.rodos.AccessRodos')

    prognosisEnd = schema.Datetime(
                        title=_(u'label_rodos_prognosisEnd', default=u'Prognosis End'),
                        description=_(u'description_rodos_prognosisEnd', default=u''),
                        required=False,
    )
    read_permission(prognosisEnd='docpool.rodos.AccessRodos')
    write_permission(prognosisEnd='docpool.rodos.AccessRodos')

    numericWeatherPredictionDate = schema.TextLine(
                        title=_(u'label_rodos_numericWeatherPredictionDate', default=u'Numeric Weather Prediction Date'),
                        description=_(u'description_rodos_numericWeatherPredictionDate', default=u''),
                        required=False,
    )
    read_permission(numericWeatherPredictionDate='docpool.rodos.AccessRodos')
    write_permission(numericWeatherPredictionDate='docpool.rodos.AccessRodos')
    dexteritytextindexer.searchable('numericWeatherPredictionDate')


class RodosDoc(FlexibleView):
    __allow_access_to_unprotected_subobjects__ = 1

    security = ClassSecurityInfo()

    appname = Rodos_APP

    def __init__(self, context):
        self.context = context
        self.request = context.REQUEST

    def _get_rodos_projectName(self):
        return getInheritedValue(self, "projectName")

    def _set_rodos_projectName(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.projectName = value

    projectName = property(_get_rodos_projectName, _set_rodos_projectName)
    
    def _get_rodos_reportId(self):
        return getInheritedValue(self, "reportId")

    def _set_rodos_reportId(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.reportId = value
    
    reportId = property(_get_rodos_reportId, _set_rodos_reportId)

    def _get_rodos_releaseSite(self):
        return getInheritedValue(self, "releaseSite")

    def _set_rodos_releaseSite(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.releaseSite = value

    releaseSite = property(_get_rodos_releaseSite, _set_rodos_releaseSite)

    def _get_rodos_releaseStart(self):
        return getInheritedValue(self, "releaseStart")

    def _set_rodos_releaseStart(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.releaseStart = value

    releaseStart = property(_get_rodos_releaseStart, _set_rodos_releaseStart)

    def _get_rodos_releaseStop(self):
        return getInheritedValue(self, "releaseStop")

    def _set_rodos_releaseStop(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.releaseStop = value

    releaseStop = property(_get_rodos_releaseStop, _set_rodos_releaseStop)

    def _get_rodos_prognosisBegin(self):
        return getInheritedValue(self, "prognosisBegin")

    def _set_rodos_prognosisBegin(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.prognosisBegin = value

    prognosisBegin = property(_get_rodos_prognosisBegin, _set_rodos_prognosisBegin)

    def _get_rodos_prognosisEnd(self):
        return getInheritedValue(self, "prognosisEnd")

    def _set_rodos_prognosisEnd(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.prognosisEnd = value

    prognosisEnd = property(_get_rodos_prognosisEnd, _set_rodos_prognosisEnd)

    def _get_rodos_numericWeatherPredictionDate(self):
        return getInheritedValue(self, "numericWeatherPredictionDate")

    def _set_rodos_numericWeatherPredictionDate(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.numericWeatherPredictionDate = value

    numericWeatherPredictionDate = property(_get_rodos_numericWeatherPredictionDate, _set_rodos_numericWeatherPredictionDate)

    def _get_rodos_model(self):
        return getInheritedValue(self, "model")

    def _set_rodos_model(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.model = value

    model = property(_get_rodos_model, _set_rodos_model)

    def _get_rodos_calculationDate(self):
        return getInheritedValue(self, "calculationDate")

    def _set_rodos_calculationDate(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.calculationDate = value

    calculationDate = property(_get_rodos_calculationDate, _set_rodos_calculationDate)

    def _get_rodos_projectUser(self):
        return getInheritedValue(self, "projectUser")

    def _set_rodos_projectUser(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.projectUser = value

    projectUser = property(_get_rodos_projectUser, _set_rodos_projectUser)


    def _get_rodos_prognosisType(self):
        return getInheritedValue(self, "prognosisType")

    def _set_rodos_prognosisType(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.prognosisType = value

    prognosisType = property(_get_rodos_prognosisType, _set_rodos_prognosisType)


    def _get_rodos_prognosisForm(self):
        return getInheritedValue(self, "prognosisForm")

    def _set_rodos_prognosisForm(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.prognosisForm = value

    prognosisForm = property(_get_rodos_prognosisForm, _set_rodos_prognosisForm)



    def isClean(self):
        """
        Is this document free for further action like publishing or transfer?
        @return:
        """
        # TODO: define if necessary. Method MUST be present in Doc behavior.
        return True
