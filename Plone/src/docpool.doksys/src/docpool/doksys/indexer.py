# -*- coding: utf-8 -*-
from plone.indexer import indexer
from Products.CMFPlone import log
from docpool.base.content.dpdocument import IDPDocument
from docpool.doksys.config import DOKSYS_APP

@indexer(IDPDocument)
def network_operator_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).network_operator
    except:
        pass

@indexer(IDPDocument)
def network_operator_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).dom
    except:
        pass

@indexer(IDPDocument)
def network_operator_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).legal_base
    except:
        pass

@indexer(IDPDocument)
def network_operator_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).measuring_program
    except:
        pass



@indexer(IDPDocument)
def sampling_begin_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).sampling_begin
    except:
        pass


@indexer(IDPDocument)
def sampling_begin_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).sampling_end
    except:
        pass

@indexer(IDPDocument)
def network_operator_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).purpose
    except:
        pass


@indexer(IDPDocument)
def network_operator_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).trajectory_start_location
    except:
        pass


@indexer(IDPDocument)
def network_operator_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).trajectory_end_location
    except:
        pass


@indexer(IDPDocument)
def network_operator_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).trajectory_start_time
    except:
        pass


@indexer(IDPDocument)
def network_operator_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).trajectory_end_time
    except:
        pass


@indexer(IDPDocument)
def network_operator_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).status
    except:
        pass


@indexer(IDPDocument)
def network_operator_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).operation_mode
    except:
        pass


@indexer(IDPDocument)
def network_operator_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).data_type
    except:
        pass


@indexer(IDPDocument)
def network_operator_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).sample_type_id
    except:
        pass


@indexer(IDPDocument)
def network_operator_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).sample_type
    except:
        pass


@indexer(IDPDocument)
def network_operator_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).measurement_category
    except:
        pass


@indexer(IDPDocument)
def network_operator_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).duration
    except:
        pass


@indexer(IDPDocument)
def network_operator_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).type
    except:
        pass


@indexer(IDPDocument)
def network_operator_indexer(obj):
    try:
        return obj.doc_extension(DOKSYS_APP).area
    except:
        pass


