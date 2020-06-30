# -*- coding: utf-8 -*-
from plone import api
from plone.app.upgrade.utils import loadMigrationProfile
import transaction


def to_1001(context):
    indexes = attributes = [
        'NetworkOperator',
        'Dom',
        'LegalBase',
        'DataType',
        'MeasurementCategory',
    ]

    loadMigrationProfile(
        context,
        'profile-docpool.doksys:to_1001',
    )

    for count, brain in enumerate(api.content.find(Type='DPDocument')):
        obj = brain.getObject()

        for attr in attributes:
            if type(getattr(obj, attr, [])) != list:
                setattr(obj, attr, [getattr(obj, attr)])

        obj.reindexObject(idxs=indexes)

        if not (count + 1) % 100:
            transaction.commit()
