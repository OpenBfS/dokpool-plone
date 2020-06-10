# -*- coding: utf-8 -*-
from plone import api
from plone.app.upgrade.utils import loadMigrationProfile
import transaction


def to_1001(context):
    catalog = api.portal.get_tool(name='portal_catalog')
    catalog.delIndex('NetworkOperator')

    loadMigrationProfile(
        context,
        'profile-docpool.doksys:to_1001',
    )

    for count, brain in enumerate(api.content.find(Type='DPDocument')):
        obj = brain.getObject()

        if type(obj.NetworkOperator) != list:
            obj.NetworkOperator = [obj.NetworkOperator]

        obj.reindexObject(idxs=['NetworkOperator'])

        if not (count + 1) % 100:
            transaction.commit()
