# -*- coding: utf-8 -*-
from docpool.base.content.dpdocument import IDPDocument
from docpool.doksys.config import DOKSYS_APP
from plone.indexer import indexer


@indexer(IDPDocument)
def network_operator_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).NetworkOperator
    except BaseException:
        pass


@indexer(IDPDocument)
def dom_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).Dom
    except BaseException:
        pass


@indexer(IDPDocument)
def legal_base_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).LegalBase
    except BaseException:
        pass


@indexer(IDPDocument)
def measuring_program_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).MeasuringProgram
    except BaseException:
        pass


@indexer(IDPDocument)
def sampling_begin_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).SamplingBegin
    except BaseException:
        pass


@indexer(IDPDocument)
def sampling_end_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).SamplingEnd
    except BaseException:
        pass


@indexer(IDPDocument)
def purpose_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).Purpose
    except BaseException:
        pass


@indexer(IDPDocument)
def trajectory_start_location_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).TrajectoryStartLocation
    except BaseException:
        pass


@indexer(IDPDocument)
def trajectory_end_location_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).TrajectoryEndLocation
    except BaseException:
        pass


@indexer(IDPDocument)
def trajectory_start_time_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).TrajectoryStartTime
    except BaseException:
        pass


@indexer(IDPDocument)
def trajectory_end_time_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).TrajectoryEndTime
    except BaseException:
        pass


@indexer(IDPDocument)
def status_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).Status
    except BaseException:
        pass


@indexer(IDPDocument)
def operation_mode_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).OperationMode
    except BaseException:
        pass


@indexer(IDPDocument)
def data_type_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).DataType
    except BaseException:
        pass


@indexer(IDPDocument)
def sample_type_id_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).SampleTypeId
    except BaseException:
        pass


@indexer(IDPDocument)
def sample_type_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).SampleType
    except BaseException:
        pass


@indexer(IDPDocument)
def measurement_category_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).MeasurementCategory
    except BaseException:
        pass


@indexer(IDPDocument)
def duration_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).Duration
    except BaseException:
        pass


@indexer(IDPDocument)
def type_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).Type
    except BaseException:
        pass


@indexer(IDPDocument)
def area_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).Area
    except BaseException:
        pass
