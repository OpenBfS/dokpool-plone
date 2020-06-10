# -*- coding: utf-8 -*-
"""Common configuration constants
"""
from AccessControl import ClassSecurityInfo
from Acquisition import aq_inner
from docpool.base import DocpoolMessageFactory as _
from docpool.base.browser.flexible_view import FlexibleView
from docpool.base.interfaces import IDocumentExtension
from docpool.doksys import DocpoolMessageFactory as _
from docpool.doksys.config import DOKSYS_APP
from plone.app.z3cform.widget import SelectFieldWidget
from plone.autoform.directives import read_permission
from plone.autoform.directives import widget
from plone.autoform.directives import write_permission
from plone.autoform.interfaces import IFormFieldProvider
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.interface import provider

# from docpool.doksys.vocabularies import SampleType


@provider(IFormFieldProvider)
class IDoksysDoc(IDocumentExtension):
    # dexteritytextindexer.searchable('NetworkOperator')  if a field is
    # supposed to be fulltext searchable

    widget(NetworkOperator=SelectFieldWidget)
    NetworkOperator = schema.List(
        title=_(u'label_doksys_network_operator', default=u'Network Operator'),
        description=_(u'description_doksys_network_operator', default=u''),
        value_type=schema.Choice(
            source="docpool.doksys.NetworkOperators",
        ),
        required=False,
        missing_value=[],
    )
    read_permission(NetworkOperator='docpool.doksys.AccessDoksys')
    write_permission(NetworkOperator='docpool.doksys.AccessDoksys')

    widget(Dom=SelectFieldWidget)
    Dom = schema.List(
        title=_(u'label_doksys_Dom', default=u'Description of Measurement'),
        description=_(u'description_doksys_Dom', default=u''),
        value_type=schema.Choice(
            source="docpool.doksys.Dom",
        ),
        required=False,
        missing_value=[],
    )
    read_permission(Dom='docpool.doksys.AccessDoksys')
    write_permission(Dom='docpool.doksys.AccessDoksys')

    widget(LegalBase=CheckBoxFieldWidget)
    LegalBase = schema.List(
        title=_(u'label_doksys_legal_base', default=u'Legal Base'),
        description=_(u'description_doksys_legal_base', default=u''),
        value_type=schema.Choice(
            source="docpool.doksys.LegalBase",
        ),
        required=False,
        missing_value=[],
    )
    read_permission(LegalBase='docpool.doksys.AccessDoksys')
    write_permission(LegalBase='docpool.doksys.AccessDoksys')

    MeasuringProgram = schema.Choice(
        title=_(
            u'label_doksys_measuring_program',
            default=u'Measuring Program'),
        description=_(u'description_doksys_measuring_program', default=u''),
        source="docpool.doksys.MeasuringProgram",
        required=False,
    )
    read_permission(MeasuringProgram='docpool.doksys.AccessDoksys')
    write_permission(MeasuringProgram='docpool.doksys.AccessDoksys')

    SamplingBegin = schema.Datetime(
        title=_(u'label_doksys_sampling_begin', default=u'Sampling Begin'),
        description=_(u'description_doksys_sampling_begin', default=u''),
        required=False,
    )
    read_permission(SamplingBegin='docpool.doksys.AccessDoksys')
    write_permission(SamplingBegin='docpool.doksys.AccessDoksys')

    SamplingEnd = schema.Datetime(
        title=_(u'label_doksys_sampling_end', default=u'Sampling End'),
        description=_(u'description_doksys_sampling_end', default=u''),
        required=False,
    )
    read_permission(SamplingEnd='docpool.doksys.AccessDoksys')
    write_permission(SamplingEnd='docpool.doksys.AccessDoksys')

    Purpose = schema.Choice(
        title=_(u'label_doksys_purpose', default=u'Purpose'),
        description=_(u'description_doksys_purpose', default=u''),
        source="docpool.doksys.Purpose",
        required=False,
    )
    read_permission(Purpose='docpool.doksys.AccessDoksys')
    write_permission(Purpose='docpool.doksys.AccessDoksys')

    TrajectoryStartLocation = schema.TextLine(
        title=_(
            u'label_doksys_trajectory_start_location',
            default=u'Trajectory Start Location',
        ),
        description=_(
            u'description_doksys_trajectory_start_location',
            default=u''),
        required=False,
    )
    read_permission(TrajectoryStartLocation='docpool.doksys.AccessDoksys')
    write_permission(TrajectoryStartLocation='docpool.doksys.AccessDoksys')

    TrajectoryEndLocation = schema.TextLine(
        title=_(
            u'label_doksys_trajectory_end_location', default=u'Trajectory End Location'
        ),
        description=_(
            u'description_doksys_trajectory_end_location',
            default=u''),
        required=False,
    )
    read_permission(TrajectoryEndLocation='docpool.doksys.AccessDoksys')
    write_permission(TrajectoryEndLocation='docpool.doksys.AccessDoksys')

    TrajectoryStartTime = schema.Datetime(
        title=_(
            u'label_doksys_trajectory_start_time', default=u'Trajectory Start Time'
        ),
        description=_(
            u'description_doksys_trajectory_start_time',
            default=u''),
        required=False,
    )
    read_permission(TrajectoryStartTime='docpool.doksys.AccessDoksys')
    write_permission(TrajectoryStartTime='docpool.doksys.AccessDoksys')

    TrajectoryEndTime = schema.Datetime(
        title=_(
            u'label_doksys_trajectory_end_time',
            default=u'Trajectory End Time'),
        description=_(u'description_doksys_trajectory_end_time', default=u''),
        required=False,
    )
    read_permission(TrajectoryEndTime='docpool.doksys.AccessDoksys')
    write_permission(TrajectoryEndTime='docpool.doksys.AccessDoksys')

    Status = schema.Choice(
        title=_(u'label_doksys_status', default=u'Status'),
        description=_(u'description_doksys_status', default=u''),
        source="docpool.doksys.Status",
        required=False,
    )
    read_permission(Status='docpool.doksys.AccessDoksys')
    write_permission(Status='docpool.doksys.AccessDoksys')

    OperationMode = schema.Choice(
        title=_(u'label_doksys_operation_mode', default=u'Operation Mode'),
        description=_(u'description_doksys_operation_mode', default=u''),
        source="docpool.doksys.OperationMode",
        default=u'Routine',
        required=True,
    )
    read_permission(OperationMode='docpool.doksys.AccessDoksys')
    write_permission(OperationMode='docpool.doksys.AccessDoksys')

    DataType = schema.Choice(
        title=_(u'label_doksys_data_type', default=u'Data Type'),
        description=_(u'description_doksys_data_type', default=u''),
        source="docpool.doksys.DataType",
        required=False,
    )
    read_permission(DataType='docpool.doksys.AccessDoksys')
    write_permission(DataType='docpool.doksys.AccessDoksys')

    SampleTypeId = schema.Choice(
        title=_(u'label_doksys_sample_type_id', default=u'Sample Type Id'),
        description=_(u'description_doksys_sample_type_id', default=u''),
        source="docpool.doksys.SampleTypeIds",
        required=False,
    )
    read_permission(SampleTypeId='docpool.doksys.AccessDoksys')
    write_permission(SampleTypeId='docpool.doksys.AccessDoksys')

    SampleType = schema.Choice(
        title=_(u'label_doksys_sample_type', default=u'Sample Type'),
        description=_(u'description_doksys_sample_type', default=u''),
        source="docpool.doksys.SampleType",
        required=False,
    )
    read_permission(SampleType='docpool.doksys.AccessDoksys')
    write_permission(SampleType='docpool.doksys.AccessDoksys')

    MeasurementCategory = schema.Choice(
        title=_(
            u'label_doksys_measurement_category',
            default=u'Measurement Category'),
        description=_(u'description_doksys_measurement_category', default=u''),
        source="docpool.doksys.MeasurementCategory",
        required=False,
    )
    read_permission(MeasurementCategory='docpool.doksys.AccessDoksys')
    write_permission(MeasurementCategory='docpool.doksys.AccessDoksys')

    Duration = schema.Choice(
        title=_(u'label_doksys_duration', default=u'Duration'),
        description=_(u'description_doksys_duration', default=u''),
        source="docpool.doksys.Duration",
        required=False,
    )
    read_permission(Duration='docpool.doksys.AccessDoksys')
    write_permission(Duration='docpool.doksys.AccessDoksys')

    InfoType = schema.Choice(
        title=_(u'label_doksys_infotype', default=u'InfoType'),
        description=_(u'description_doksys_infotype', default=u''),
        source="docpool.doksys.InfoType",
        required=False,
    )
    read_permission(InfoType='docpool.doksys.AccessDoksys')
    write_permission(InfoType='docpool.doksys.AccessDoksys')

    Area = schema.Choice(
        title=_(u'label_doksys_area', default=u'Area'),
        description=_(u'description_doksys_area', default=u''),
        source="docpool.doksys.Area",
        required=False,
    )
    read_permission(Area='docpool.doksys.AccessDoksys')
    write_permission(Area='docpool.doksys.AccessDoksys')


class DoksysDoc(FlexibleView):
    __allow_access_to_unprotected_subobjects__ = 1

    security = ClassSecurityInfo()

    appname = DOKSYS_APP

    def __init__(self, context):
        self.context = context
        self.request = context.REQUEST

    def _get_NetworkOperator(self):
        return self.context.NetworkOperator

    def _set_NetworkOperator(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.NetworkOperator = value

    NetworkOperator = property(_get_NetworkOperator, _set_NetworkOperator)

    def _get_Dom(self):
        return self.context.Dom

    def _set_Dom(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.Dom = value

    Dom = property(_get_Dom, _set_Dom)

    def _get_LegalBase(self):
        return self.context.LegalBase

    def _set_LegalBase(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.LegalBase = value

    LegalBase = property(_get_LegalBase, _set_LegalBase)

    def _get_SamplingBegin(self):
        return self.context.SamplingBegin

    def _set_SamplingBegin(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.SamplingBegin = value

    SamplingBegin = property(_get_SamplingBegin, _set_SamplingBegin)

    def _get_SamplingEnd(self):
        return self.context.SamplingEnd

    def _set_SamplingEnd(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.SamplingEnd = value

    SamplingEnd = property(_get_SamplingEnd, _set_SamplingEnd)

    def _get_MeasuringProgram(self):
        return self.context.MeasuringProgram

    def _set_MeasuringProgram(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.MeasuringProgram = value

    MeasuringProgram = property(_get_MeasuringProgram, _set_MeasuringProgram)

    def _get_Purpose(self):
        return self.context.Purpose

    def _set_Purpose(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.Purpose = value

    Purpose = property(_get_Purpose, _set_Purpose)

    def _get_TrajectoryStartLocation(self):
        return self.context.TrajectoryStartLocation

    def _set_TrajectoryStartLocation(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.TrajectoryStartLocation = value

    TrajectoryStartLocation = property(
        _get_TrajectoryStartLocation, _set_TrajectoryStartLocation
    )

    def _get_TrajectoryEndLocation(self):
        return self.context.TrajectoryEndLocation

    def _set_TrajectoryEndLocation(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.TrajectoryEndLocation = value

    TrajectoryEndLocation = property(
        _get_TrajectoryEndLocation, _set_TrajectoryEndLocation
    )

    def _get_TrajectoryStartTime(self):
        return self.context.TrajectoryStartTime

    def _set_TrajectoryStartTime(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.TrajectoryStartTime = value

    TrajectoryStartTime = property(
        _get_TrajectoryStartTime,
        _set_TrajectoryStartTime)

    def _get_TrajectoryEndTime(self):
        return self.context.TrajectoryEndTime

    def _set_TrajectoryEndTime(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.TrajectoryEndTime = value

    TrajectoryEndTime = property(
        _get_TrajectoryEndTime,
        _set_TrajectoryEndTime)

    def _get_Status(self):
        return self.context.Status

    def _set_Status(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.Status = value

    Status = property(_get_Status, _set_Status)

    def _get_OperationMode(self):
        return self.context.OperationMode

    def _set_OperationMode(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.OperationMode = value

    OperationMode = property(_get_OperationMode, _set_OperationMode)

    def _get_DataType(self):
        return self.context.DataType

    def _set_DataType(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.DataType = value

    DataType = property(_get_DataType, _set_DataType)

    def _get_SampleTypeId(self):
        return self.context.SampleTypeId

    def _set_SampleTypeId(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.SampleTypeId = value

    SampleTypeId = property(_get_SampleTypeId, _set_SampleTypeId)

    def _get_SampleType(self):
        return self.context.SampleType

    def _set_SampleType(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.SampleType = value

    SampleType = property(_get_SampleType, _set_SampleType)

    def _get_MeasurementCategory(self):
        return self.context.MeasurementCategory

    def _set_MeasurementCategory(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.MeasurementCategory = value

    MeasurementCategory = property(
        _get_MeasurementCategory,
        _set_MeasurementCategory)

    def _get_Duration(self):
        return self.context.Duration

    def _set_Duration(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.Duration = value

    Duration = property(_get_Duration, _set_Duration)

    def _get_InfoType(self):
        return self.context.InfoType

    def _set_InfoType(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.InfoType = value

    InfoType = property(_get_InfoType, _set_InfoType)

    def _get_Type(self):
        return self.context.Type

    def _set_Type(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.Type = value

    Type = property(_get_Type, _set_Type)

    def _get_Area(self):
        return self.context.Area

    def _set_Area(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.Area = value

    Area = property(_get_Area, _set_Area)

    def isClean(self):
        """
        Is this document free for further action like publishing or transfer?
        @return:
        """
        # TODO: define if necessary. Method MUST be present in Doc behavior.
        return True
