# -*- coding: utf-8 -*-
from .utils import set_local_roles
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
        try:
            api.content.move(docpool['contentconfig']['help'], docpool)
        except KeyError:
            api.content.copy(help, docpool)
        set_local_roles(
            docpool,
            docpool['help'],
            '{0}_ContentAdministrators',
            ['ContentAdmin']
        )

    api.content.delete(help)
