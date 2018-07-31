# -*- coding: utf-8 -*-
"""Common configuration constants
"""
from collective import dexteritytextindexer
from plone.autoform.interfaces import IFormFieldProvider
from plone.autoform.directives import read_permission, write_permission
from plone.directives import form
from zope.interface import provider, implementer
from zope import schema
from docpool.base import DocpoolMessageFactory as _
from docpool.base.browser.flexible_view import FlexibleView
from docpool.doksys.config import DOKSYS_APP
from AccessControl import ClassSecurityInfo
from docpool.base.interfaces import IDocumentExtension

from docpool.doksys import DocpoolMessageFactory as _
from docpool.doksys.vocabularies import sample_type

from Acquisition import aq_inner


@provider(IFormFieldProvider)
class IDoksysDoc(IDocumentExtension):
    # dexteritytextindexer.searchable('network_operator')  if a field is supposed to be fulltext searchable

    network_operator = schema.Choice(
        title=_(u'label_doksys_network_operator', default=u'Network Operator'),
        description=_(u'description_doksys_network_operator', default=u''),
        source="docpool.doksys.NetworkOperators",
        required=False,
    )
    read_permission(network_operator='docpool.doksys.AccessDoksys')
    write_permission(network_operator='docpool.doksys.AccessDoksys')

    dom = schema.Choice(
        title=_(u'label_doksys_dom', default=u'Description of Measurement'),
        description=_(u'description_doksys_dom', default=u''),
        source="docpool.doksys.Dom",
        required=False,

    )
    read_permission(dom='docpool.doksys.AccessDoksys')
    write_permission(dom='docpool.doksys.AccessDoksys')

    legal_base = schema.Choice(
        title=_(u'label_doksys_legal_base', default=u'Legal Base'),
        description=_(u'description_doksys_legal_base', default=u''),
        source="docpool.doksys.LegalBase",
        required=False,
    )
    read_permission(legal_base='docpool.doksys.AccessDoksys')
    write_permission(legal_base='docpool.doksys.AccessDoksys')

    measuring_program = schema.Choice(
        title=_(u'label_doksys_measuring_program', default=u'Measuring Program'),
        description=_(u'description_doksys_measuring_program', default=u''),
        source="docpool.doksys.MeasuringProgram",
        required=False,
    )
    read_permission(measuring_program='docpool.doksys.AccessDoksys')
    write_permission(measuring_program='docpool.doksys.AccessDoksys')

    sampling_begin = schema.Datetime(
        title=_(u'label_doksys_sampling_begin', default=u'Sampling Begin'),
        description=_(u'description_doksys_sampling_begin', default=u''),
        required=False,
    )
    read_permission(sampling_begin='docpool.doksys.AccessDoksys')
    write_permission(sampling_begin='docpool.doksys.AccessDoksys')

    sampling_end = schema.Datetime(
        title=_(u'label_doksys_sampling_end', default=u'Sampling End'),
        description=_(u'description_doksys_sampling_end', default=u''),
        required=False,
    )
    read_permission(sampling_end='docpool.doksys.AccessDoksys')
    write_permission(sampling_end='docpool.doksys.AccessDoksys')

    purpose = schema.Choice(
        title=_(u'label_doksys_purpose', default=u'Purpose'),
        description=_(u'description_doksys_purpose', default=u''),
        source="docpool.doksys.Purpose",
        required=False,
    )
    read_permission(purpose='docpool.doksys.AccessDoksys')
    write_permission(purpose='docpool.doksys.AccessDoksys')

    trajectory_start_location = schema.TextLine(
        title=_(u'label_doksys_trajectory_start_location', default=u'Trajectory Start Location'),
        description=_(u'description_doksys_trajectory_start_location', default=u''),
        required=False,
    )
    read_permission(trajectory_start_location='docpool.doksys.AccessDoksys')
    write_permission(trajectory_start_location='docpool.doksys.AccessDoksys')

    trajectory_end_location = schema.TextLine(
        title=_(u'label_doksys_trajectory_end_location', default=u'Trajectory End Location'),
        description=_(u'description_doksys_trajectory_end_location', default=u''),
        required=False,
    )
    read_permission(trajectory_end_location='docpool.doksys.AccessDoksys')
    write_permission(trajectory_end_location='docpool.doksys.AccessDoksys')

    trajectory_start_time = schema.Datetime(
        title=_(u'label_doksys_trajectory_start_time', default=u'Trajectory Start Time'),
        description=_(u'description_doksys_trajectory_start_time', default=u''),
        required=False,
    )
    read_permission(trajectory_start_time='docpool.doksys.AccessDoksys')
    write_permission(trajectory_start_time='docpool.doksys.AccessDoksys')

    trajectory_end_time = schema.Datetime(
        title=_(u'label_doksys_trajectory_end_time', default=u'Trajectory End Time'),
        description=_(u'description_doksys_trajectory_end_time', default=u''),
        required=False,
    )
    read_permission(trajectory_end_time='docpool.doksys.AccessDoksys')
    write_permission(trajectory_end_time='docpool.doksys.AccessDoksys')

    status = schema.Choice(
        title=_(u'label_doksys_status', default=u'Status'),
        description=_(u'description_doksys_status', default=u''),
        source="docpool.doksys.Status",
        required=False,
    )
    read_permission(status='docpool.doksys.AccessDoksys')
    write_permission(status='docpool.doksys.AccessDoksys')

    operation_mode = schema.Choice(
        title=_(u'label_doksys_operation_mode', default=u'Operation Mode'),
        description=_(u'description_doksys_operation_mode', default=u''),
        source="docpool.doksys.OperationMode",
        required=False,
    )
    read_permission(operation_mode='docpool.doksys.AccessDoksys')
    write_permission(operation_mode='docpool.doksys.AccessDoksys')

    data_type = schema.Choice(
        title=_(u'label_doksys_data_type', default=u'Data Type'),
        description=_(u'description_doksys_data_type', default=u''),
        source="docpool.doksys.DataType",
        required=False,
    )
    read_permission(data_type='docpool.doksys.AccessDoksys')
    write_permission(data_type='docpool.doksys.AccessDoksys')

    sample_type_id = schema.Choice(
        title=_(u'label_doksys_sample_type_id', default=u'Sample Type Id'),
        description=_(u'description_doksys_sample_type_id', default=u''),
        source="docpool.doksys.SampleTypeIds",
        required=False,
    )
    read_permission(sample_type_id='docpool.doksys.AccessDoksys')
    write_permission(sample_type_id='docpool.doksys.AccessDoksys')

    sample_type = schema.Choice(
        title=_(u'label_doksys_sample_type', default=u'Sample Type'),
        description=_(u'description_doksys_sample_type', default=u''),
        source= "docpool.doksys.SampleTypes",
        required=False,
    )
    read_permission(sample_type='docpool.doksys.AccessDoksys')
    write_permission(sample_type='docpool.doksys.AccessDoksys')

    measurement_category = schema.Choice(
        title=_(u'label_doksys_measurement_category', default=u'Measurement Category'),
        description=_(u'description_doksys_measurement_category', default=u''),
        source="docpool.doksys.MeasurementCategory",
        required=False,
    )
    read_permission(measurement_category='docpool.doksys.AccessDoksys')
    write_permission(measurement_category='docpool.doksys.AccessDoksys')

    duration = schema.Choice(
        title=_(u'label_doksys_duration', default=u'Duration'),
        description=_(u'description_doksys_duration', default=u''),
        source="docpool.doksys.Duration",
        required=False,
    )
    read_permission(duration='docpool.doksys.AccessDoksys')
    write_permission(duration='docpool.doksys.AccessDoksys')

    type = schema.Choice(
        title=_(u'label_doksys_duration', default=u'Type'),
        description=_(u'description_doksys_type', default=u''),
        source="docpool.doksys.Type",
        required=False,
    )
    read_permission(duration='docpool.doksys.AccessDoksys')
    write_permission(duration='docpool.doksys.AccessDoksys')

    area = schema.Choice(
        title=_(u'label_doksys_area', default=u'Area'),
        description=_(u'description_doksys_area', default=u''),
        source="docpool.doksys.Area",
        required=False,
    )
    read_permission(area='docpool.doksys.AccessDoksys')
    write_permission(area='docpool.doksys.AccessDoksys')

class DoksysDoc(FlexibleView):
    __allow_access_to_unprotected_subobjects__ = 1

    security = ClassSecurityInfo()

    appname = DOKSYS_APP

    def __init__(self, context):
        self.context = context
        self.request = context.REQUEST

    def _get_network_operator(self):
        return self.context.network_operator

    def _set_network_operator(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.network_operator = value

    network_operator = property(_get_network_operator, _set_network_operator)

    def _get_dom(self):
        return self.context.dom

    def _set_dom(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.dom = value

    dom = property(_get_dom, _set_dom)

    def _get_legal_base(self):
        return self.context.legal_base

    def _set_legal_base(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.legal_base = value

    legal_base = property(_get_legal_base, _set_legal_base)

    def _get_sampling_begin(self):
        return self.context.sampling_begin

    def _set_sampling_begin(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.sampling_begin = value

    sampling_begin = property(_get_sampling_begin, _set_sampling_begin)

    def _get_sampling_end(self):
        return self.context.sampling_end

    def _set_sampling_end(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.sampling_end = value

    sampling_end = property(_get_sampling_end, _set_sampling_end)

    def _get_measuring_program(self):
        return self.context.measuring_program

    def _set_measuring_program(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.measuring_program = value

    measuring_program = property(_get_measuring_program, _set_measuring_program)

    def _get_purpose(self):
        return self.context.purpose

    def _set_purpose(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.purpose = value

    purpose = property(_get_purpose, _set_purpose)

    def _get_trajectory_start_location(self):
        return self.context.trajectory_start_location

    def _set_trajectory_start_location(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.trajectory_start_location = value

    trajectory_start_location = property(_get_trajectory_start_location, _set_trajectory_start_location)

    def _get_trajectory_end_location(self):
        return self.context.trajectory_end_location

    def _set_trajectory_end_location(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.trajectory_end_location = value

    trajectory_end_location = property(_get_trajectory_end_location, _set_trajectory_end_location)

    def _get_trajectory_start_time(self):
        return self.context.trajectory_start_time

    def _set_trajectory_start_time(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.trajectory_start_time = value

    trajectory_start_time = property(_get_trajectory_start_time, _set_trajectory_start_time)

    def _get_trajectory_end_time(self):
        return self.context.trajectory_end_time

    def _set_trajectory_end_time(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.trajectory_end_time = value

    trajectory_end_time = property(_get_trajectory_end_time, _set_trajectory_end_time)

    def _get_status(self):
        return self.context.status

    def _set_status(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.status = value

    status = property(_get_status, _set_status)

    def _get_operation_mode(self):
        return self.context.operation_mode

    def _set_operation_mode(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.operation_mode = value

    operation_mode = property(_get_operation_mode, _set_operation_mode)

    def _get_data_type(self):
        return self.context.data_type

    def _set_data_type(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.data_type = value

    data_type = property(_get_data_type, _set_data_type)

    def _get_sample_type_id(self):
        return self.context.sample_type_id

    def _set_sample_type_id(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.sample_type_id = value

    sample_type_id = property(_get_sample_type_id, _set_sample_type_id)

    def _get_sample_type(self):
        return self.context.sample_type

    def _set_sample_type(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.sample_type = value

    sample_type = property(_get_sample_type, _set_sample_type)

    def _get_measurement_category(self):
        return self.context.measurement_category

    def _set_measurement_category(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.measurement_category = value

    measurement_category = property(_get_measurement_category, _set_measurement_category)

    def _get_duration(self):
        return self.context.duration

    def _set_duration(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.duration = value

    duration = property(_get_duration, _set_duration)

    def _get_type(self):
        return self.context.type

    def _set_type(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.type = value

    type = property(_get_type, _set_type)

    def _get_area(self):
        return self.context.area

    def _set_area(self, value):
        if not value:
            return
        context = aq_inner(self.context)
        context.area = value

    area = property(_get_area, _set_area)

    def isClean(self):
        """
        Is this document free for further action like publishing or transfer?
        @return:
        """
        # TODO: define if necessary. Method MUST be present in Doc behavior.
        return True


