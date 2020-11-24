# -*- coding: utf-8 -*-
from plone import api
from plone.app.upgrade.utils import loadMigrationProfile


def to_1001(context):
    loadMigrationProfile(
        context,
        'profile-docpool.config:to_1001',
    )

    portal = api.portal.get()
    if 'help' not in portal['contentconfig']:
        return

    help = portal['contentconfig']['help']

    for brain in api.content.find(portal_type='DocumentPool'):
        docpool = brain.getObject()
        api.content.copy(help, docpool['contentconfig'])

    api.content.delete(help)
