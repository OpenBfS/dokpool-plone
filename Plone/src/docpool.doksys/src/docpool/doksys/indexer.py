# -*- coding: utf-8 -*-
from docpool.base.content.dpdocument import IDPDocument
from docpool.doksys.config import DOKSYS_APP
from plone.indexer import indexer


@indexer(IDPDocument)
def network_operator_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).NetworkOperator
    except:
        pass


@indexer(IDPDocument)
def dom_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).Dom
    except:
        pass


@indexer(IDPDocument)
def legal_base_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).LegalBase
    except:
        pass


@indexer(IDPDocument)
def measuring_program_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).MeasuringProgram
    except:
        pass


@indexer(IDPDocument)
def sampling_begin_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).SamplingBegin
    except:
        pass


@indexer(IDPDocument)
def sampling_end_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).SamplingEnd
    except:
        pass


@indexer(IDPDocument)
def purpose_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).Purpose
    except:
        pass


@indexer(IDPDocument)
def trajectory_start_location_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).TrajectoryStartLocation
    except:
        pass


@indexer(IDPDocument)
def trajectory_end_location_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).TrajectoryEndLocation
    except:
        pass


@indexer(IDPDocument)
def trajectory_start_time_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).TrajectoryStartTime
    except:
        pass


@indexer(IDPDocument)
def trajectory_end_time_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).TrajectoryEndTime
    except:
        pass


@indexer(IDPDocument)
def status_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).Status
    except:
        pass


@indexer(IDPDocument)
def operation_mode_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).OperationMode
    except:
        pass


@indexer(IDPDocument)
def data_type_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).DataType
    except:
        pass


@indexer(IDPDocument)
def sample_type_id_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).SampleTypeId
    except:
        pass


@indexer(IDPDocument)
def sample_type_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).SampleType
    except:
        pass


@indexer(IDPDocument)
def measurement_category_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).MeasurementCategory
    except:
        pass


@indexer(IDPDocument)
def duration_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).Duration
    except:
        pass


@indexer(IDPDocument)
def type_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).Type
    except:
        pass


@indexer(IDPDocument)
def area_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).Area
    except:
        pass
