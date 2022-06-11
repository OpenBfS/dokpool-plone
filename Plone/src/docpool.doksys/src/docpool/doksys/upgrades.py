from plone import api
from plone.app.upgrade.utils import loadMigrationProfile
import transaction


def to_1001(context):
    attributes = [
        'NetworkOperator',
        'Dom',
        'LegalBase',
        'DataType',
        'SampleType',
        'MeasurementCategory',
    ]
    indexes = attributes + ['SampleTypeId']

    loadMigrationProfile(
        context,
        'profile-docpool.doksys:to_1001',
    )

    for count, brain in enumerate(api.content.find(portal_type='DPDocument')):
        obj = brain.getObject()

        for attr in attributes:
            if type(getattr(obj, attr, [])) != list:
                setattr(obj, attr, [getattr(obj, attr)])

        if hasattr(obj, 'SampleTypeId'):
            obj.SampleType = [obj.SampleTypeId]
            del obj.SampleTypeId

        obj.reindexObject(idxs=indexes)

        if not (count + 1) % 100:
            transaction.commit()
