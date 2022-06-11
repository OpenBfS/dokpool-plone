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
from plone.autoform.directives import read_permission, widget, write_permission
from plone.autoform.interfaces import IFormFieldProvider
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema
from zope.component import getUtility
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory


@provider(IFormFieldProvider)
class IDoksysDoc(IDocumentExtension):
    # dexteritytextindexer.searchable('NetworkOperator')  if a field is
    # supposed to be fulltext searchable

    OperationMode = schema.Choice(
        title=_("label_doksys_operation_mode", default="Operation Mode"),
        description=_("description_doksys_operation_mode", default=""),
        source="docpool.doksys.OperationMode",
        default="Routine",
        required=True,
    )
    read_permission(OperationMode="docpool.doksys.AccessDoksys")
    write_permission(OperationMode="docpool.doksys.AccessDoksys")

    Purpose = schema.Choice(
        title=_("label_doksys_purpose", default="Purpose"),
        description=_("description_doksys_purpose", default=""),
        source="docpool.doksys.Purpose",
        required=False,
    )
    read_permission(Purpose="docpool.doksys.AccessDoksys")
    write_permission(Purpose="docpool.doksys.AccessDoksys")

    widget(NetworkOperator=SelectFieldWidget)
    NetworkOperator = schema.List(
        title=_("label_doksys_network_operator", default="Network Operator"),
        description=_("description_doksys_network_operator", default=""),
        value_type=schema.Choice(
            source="docpool.doksys.NetworkOperators",
        ),
        required=False,
        missing_value=[],
    )
    read_permission(NetworkOperator="docpool.doksys.AccessDoksys")
    write_permission(NetworkOperator="docpool.doksys.AccessDoksys")

    widget(LegalBase=CheckBoxFieldWidget)
    LegalBase = schema.List(
        title=_("label_doksys_legal_base", default="Legal Base"),
        description=_("description_doksys_legal_base", default=""),
        value_type=schema.Choice(
            source="docpool.doksys.LegalBase",
        ),
        required=False,
        missing_value=[],
    )
    read_permission(LegalBase="docpool.doksys.AccessDoksys")
    write_permission(LegalBase="docpool.doksys.AccessDoksys")

    MeasuringProgram = schema.Choice(
        title=_("label_doksys_measuring_program", default="Measuring Program"),
        description=_("description_doksys_measuring_program", default=""),
        source="docpool.doksys.MeasuringProgram",
        required=False,
    )
    read_permission(MeasuringProgram="docpool.doksys.AccessDoksys")
    write_permission(MeasuringProgram="docpool.doksys.AccessDoksys")

    widget(DataType=CheckBoxFieldWidget)
    DataType = schema.List(
        title=_("label_doksys_data_type", default="Data Type"),
        description=_("description_doksys_data_type", default=""),
        value_type=schema.Choice(
            source="docpool.doksys.DataType",
        ),
        required=False,
        missing_value=[],
    )
    read_permission(DataType="docpool.doksys.AccessDoksys")
    write_permission(DataType="docpool.doksys.AccessDoksys")

    widget(SampleType=SelectFieldWidget)
    SampleType = schema.List(
        title=_("label_doksys_sample_type", default="Sample Type"),
        description=_("description_doksys_sample_type", default=""),
        value_type=schema.Choice(
            source="docpool.doksys.SampleType",
        ),
        required=False,
        missing_value=[],
    )
    read_permission(SampleType="docpool.doksys.AccessDoksys")
    write_permission(SampleType="docpool.doksys.AccessDoksys")

    widget(Dom=SelectFieldWidget)
    Dom = schema.List(
        title=_("label_doksys_Dom", default="Description of Measurement"),
        description=_("description_doksys_Dom", default=""),
        value_type=schema.Choice(
            source="docpool.doksys.Dom",
        ),
        required=False,
        missing_value=[],
    )
    read_permission(Dom="docpool.doksys.AccessDoksysDOM")
    write_permission(Dom="docpool.doksys.AccessDoksysDOM")

    InfoType = schema.Choice(
        title=_("label_doksys_infotype", default="InfoType"),
        description=_("description_doksys_infotype", default=""),
        source="docpool.doksys.InfoType",
        required=False,
    )
    read_permission(InfoType="docpool.doksys.AccessDoksys")
    write_permission(InfoType="docpool.doksys.AccessDoksys")

    widget(MeasurementCategory=SelectFieldWidget)
    MeasurementCategory = schema.List(
        title=_("label_doksys_measurement_category", default="Measurement Category"),
        description=_("description_doksys_measurement_category", default=""),
        value_type=schema.Choice(
            source="docpool.doksys.MeasurementCategory",
        ),
        required=False,
        missing_value=[],
    )
    read_permission(MeasurementCategory="docpool.doksys.AccessDoksys")
    write_permission(MeasurementCategory="docpool.doksys.AccessDoksys")

    Duration = schema.Choice(
        title=_("label_doksys_duration", default="Duration"),
        description=_("description_doksys_duration", default=""),
        source="docpool.doksys.Duration",
        required=False,
    )
    read_permission(Duration="docpool.doksys.AccessDoksys")
    write_permission(Duration="docpool.doksys.AccessDoksys")

    Status = schema.Choice(
        title=_("label_doksys_status", default="Status"),
        description=_("description_doksys_status", default=""),
        source="docpool.doksys.Status",
        required=False,
    )
    read_permission(Status="docpool.doksys.AccessDoksys")
    write_permission(Status="docpool.doksys.AccessDoksys")

    SamplingBegin = schema.Datetime(
        title=_("label_doksys_sampling_begin", default="Sampling Begin"),
        description=_("description_doksys_sampling_begin", default=""),
        required=False,
    )
    read_permission(SamplingBegin="docpool.doksys.AccessDoksys")
    write_permission(SamplingBegin="docpool.doksys.AccessDoksys")

    SamplingEnd = schema.Datetime(
        title=_("label_doksys_sampling_end", default="Sampling End"),
        description=_("description_doksys_sampling_end", default=""),
        required=False,
    )
    read_permission(SamplingEnd="docpool.doksys.AccessDoksys")
    write_permission(SamplingEnd="docpool.doksys.AccessDoksys")

    TrajectoryStartLocation = schema.TextLine(
        title=_(
            "label_doksys_trajectory_start_location",
            default="Trajectory Start Location",
        ),
        description=_("description_doksys_trajectory_start_location", default=""),
        required=False,
    )
    read_permission(TrajectoryStartLocation="docpool.doksys.AccessDoksys")
    write_permission(TrajectoryStartLocation="docpool.doksys.AccessDoksys")

    TrajectoryEndLocation = schema.TextLine(
        title=_(
            "label_doksys_trajectory_end_location", default="Trajectory End Location"
        ),
        description=_("description_doksys_trajectory_end_location", default=""),
        required=False,
    )
    read_permission(TrajectoryEndLocation="docpool.doksys.AccessDoksys")
    write_permission(TrajectoryEndLocation="docpool.doksys.AccessDoksys")

    TrajectoryStartTime = schema.Datetime(
        title=_("label_doksys_trajectory_start_time", default="Trajectory Start Time"),
        description=_("description_doksys_trajectory_start_time", default=""),
        required=False,
    )
    read_permission(TrajectoryStartTime="docpool.doksys.AccessDoksys")
    write_permission(TrajectoryStartTime="docpool.doksys.AccessDoksys")

    TrajectoryEndTime = schema.Datetime(
        title=_("label_doksys_trajectory_end_time", default="Trajectory End Time"),
        description=_("description_doksys_trajectory_end_time", default=""),
        required=False,
    )
    read_permission(TrajectoryEndTime="docpool.doksys.AccessDoksys")
    write_permission(TrajectoryEndTime="docpool.doksys.AccessDoksys")

    Area = schema.Choice(
        title=_("label_doksys_area", default="Area"),
        description=_("description_doksys_area", default=""),
        source="docpool.doksys.Area",
        required=False,
    )
    read_permission(Area="docpool.doksys.AccessDoksys")
    write_permission(Area="docpool.doksys.AccessDoksys")


class DoksysDoc(FlexibleView):
    __allow_access_to_unprotected_subobjects__ = 1

    security = ClassSecurityInfo()

    appname = DOKSYS_APP

    def __init__(self, context):
        self.context = context
        self.request = context.REQUEST

    def _get_Purpose(self):
        return self.context.Purpose

    def _set_Purpose(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.Purpose = value

    Purpose = property(_get_Purpose, _set_Purpose)

    def _get_OperationMode(self):
        return self.context.OperationMode

    def _set_OperationMode(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.OperationMode = value

    OperationMode = property(_get_OperationMode, _set_OperationMode)

    def _get_NetworkOperator(self):
        return self.context.NetworkOperator

    def _set_NetworkOperator(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.NetworkOperator = value

    NetworkOperator = property(_get_NetworkOperator, _set_NetworkOperator)

    def _get_LegalBase(self):
        return self.context.LegalBase

    def _set_LegalBase(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.LegalBase = value

    LegalBase = property(_get_LegalBase, _set_LegalBase)

    def _get_MeasuringProgram(self):
        return self.context.MeasuringProgram

    def _set_MeasuringProgram(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.MeasuringProgram = value

    MeasuringProgram = property(_get_MeasuringProgram, _set_MeasuringProgram)

    def _get_DataType(self):
        return self.context.DataType

    def _set_DataType(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.DataType = value

    DataType = property(_get_DataType, _set_DataType)

    def _get_SampleType(self):
        return self.context.SampleType

    def _set_SampleType(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.SampleType = value

    SampleType = property(_get_SampleType, _set_SampleType)

    def sample_type_display(self):
        voc = getUtility(IVocabularyFactory, "docpool.doksys.SampleType")()
        return ", ".join(voc.getTerm(i).title for i in self.SampleType)

    def _get_Dom(self):
        return self.context.Dom

    def _set_Dom(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.Dom = value

    Dom = property(_get_Dom, _set_Dom)

    def _get_InfoType(self):
        return self.context.InfoType

    def _set_InfoType(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.InfoType = value

    InfoType = property(_get_InfoType, _set_InfoType)

    def _get_MeasurementCategory(self):
        return self.context.MeasurementCategory

    def _set_MeasurementCategory(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.MeasurementCategory = value

    MeasurementCategory = property(_get_MeasurementCategory, _set_MeasurementCategory)

    def _get_Duration(self):
        return self.context.Duration

    def _set_Duration(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.Duration = value

    Duration = property(_get_Duration, _set_Duration)

    def _get_Status(self):
        return self.context.Status

    def _set_Status(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.Status = value

    Status = property(_get_Status, _set_Status)

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

    TrajectoryStartTime = property(_get_TrajectoryStartTime, _set_TrajectoryStartTime)

    def _get_TrajectoryEndTime(self):
        return self.context.TrajectoryEndTime

    def _set_TrajectoryEndTime(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.TrajectoryEndTime = value

    TrajectoryEndTime = property(_get_TrajectoryEndTime, _set_TrajectoryEndTime)

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
