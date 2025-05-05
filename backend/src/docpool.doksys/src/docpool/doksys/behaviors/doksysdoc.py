from AccessControl import ClassSecurityInfo
from docpool.base.browser.flexible_view import FlexibleView
from docpool.base.interfaces import IDocumentExtension
from docpool.base.utils import ContextProperty
from docpool.doksys import DocpoolMessageFactory as _
from docpool.doksys.config import DOKSYS_APP
from plone.app.z3cform.widget import SelectFieldWidget
from plone.autoform.directives import read_permission
from plone.autoform.directives import widget
from plone.autoform.directives import write_permission
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
        title=_("label_doksys_trajectory_end_location", default="Trajectory End Location"),
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

    OperationMode = ContextProperty("OperationMode", skip_empty=True)
    Purpose = ContextProperty("Purpose", skip_empty=True)
    NetworkOperator = ContextProperty("NetworkOperator", default=[], skip_empty=True)
    LegalBase = ContextProperty("LegalBase", default=[], skip_empty=True)
    MeasuringProgram = ContextProperty("MeasuringProgram", skip_empty=True)
    DataType = ContextProperty("context.DataType", default=[], skip_empty=True)
    SampleType = ContextProperty("SampleType", default=[], skip_empty=True)
    Dom = ContextProperty("Dom", default=[], skip_empty=True)
    InfoType = ContextProperty("InfoType", skip_empty=True)
    MeasurementCategory = ContextProperty("MeasurementCategory", default=[], skip_empty=True)
    Duration = ContextProperty("Duration", skip_empty=True)
    Status = ContextProperty("Status", skip_empty=True)
    SamplingBegin = ContextProperty("SamplingBegin", skip_empty=True)
    SamplingEnd = ContextProperty("SamplingEnd", skip_empty=True)
    TrajectoryStartLocation = ContextProperty("TrajectoryStartLocation", skip_empty=True)
    TrajectoryEndLocation = ContextProperty("TrajectoryEndLocation", skip_empty=True)
    TrajectoryStartTime = ContextProperty("TrajectoryStartTime", skip_empty=True)
    TrajectoryEndTime = ContextProperty("TrajectoryEndTime", skip_empty=True)
    Area = ContextProperty("Area", skip_empty=True)

    def sample_type_display(self):
        voc = getUtility(IVocabularyFactory, "docpool.doksys.SampleType")()
        return ", ".join(voc.getTerm(i).title for i in self.SampleType)

    def isClean(self):
        """
        Is this document free for further action like publishing or transfer?
        @return:
        """
        # TODO: define if necessary. Method MUST be present in Doc behavior.
        return True
