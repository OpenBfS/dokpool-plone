# -*- coding: utf-8 -*-
from __future__ import print_function
from docpool.config.utils import CHILDREN
from docpool.config.utils import createPloneObjects
from docpool.config.utils import ID
from docpool.config.utils import TITLE
from docpool.config.utils import TYPE
from plone import api
from plone.app.textfield.value import RichTextValue
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType

import transaction


def install(plonesite):
    """
    """
    fresh = True
    if plonesite.hasObject("rei"):
        fresh = False  # It's a reinstall
    configUsers(plonesite, fresh)
    createStructure(plonesite, fresh)


def configUsers(plonesite, fresh):
    """
    """
    if fresh:
        mtool = getToolByName(plonesite, "portal_membership")
        mtool.addMember(
            'reiadmin',
            'REI Administrator (global)',
            ['Site Administrator', 'Member'],
            [],
        )
        reiadmin = mtool.getMemberById('reiadmin')
        reiadmin.setMemberProperties({"fullname": 'REI Administrator'})
        reiadmin.setSecurityProfile(password="admin")
        mtool.addMember(
            'reimanager', 'REI Manager (global)', [
                'Manager', 'Member'], [])
        reimanager = mtool.getMemberById('reimanager')
        reimanager.setMemberProperties({"fullname": 'REI Manager'})
        reimanager.setSecurityProfile(password="admin")
        # Role from rolemap.xml
        api.user.grant_roles(username='reimanager', roles=['REIUser'])
        api.user.grant_roles(username='reiadmin', roles=['REIUser'])
        api.user.grant_roles(username='dpmanager', roles=['REIUser'])
        api.user.grant_roles(username='dpadmin', roles=['REIUser'])


def createStructure(plonesite, fresh):
    changeREINavigation(plonesite, fresh)
    s = api.content.get(path='/berichte')
    s.relatedItems = ""
    s.manage_addProperty('text', '', 'string')
    transaction.commit()
    create_all_collection(plonesite)
    create_all_private_collection(plonesite)
    transaction.commit()
    changeREIDocTypes(plonesite, fresh)
    transaction.commit()


def createREINavigation(plonesite, fresh):
    createPloneObjects(plonesite, BASICSTRUCTURE, fresh)
    #    create_all_private_collection(plonesite)
    create_all_collection(plonesite)
    print("struktur angelegt")


def createREIDocTypes(plonesite, fresh):
    createPloneObjects(plonesite.config.dtypes, DTYPES, fresh)
    print("REI Bericht angelegt")


def changeREINavigation(plonesite, fresh):
    createPloneObjects(plonesite, BASICSTRUCTURE, fresh)


def changeREIDocTypes(plonesite, fresh):
    createPloneObjects(plonesite.config.dtypes, DTYPES, fresh)


def create_all_collection(plonesite):
    container = api.content.get(path='/berichte')
    #    container.manage_addProperty('text', '', 'string')
    title = 'Alle'
    description = 'Alle REI Berichte'
    _createObjectByType(
        'Collection', container, id='all', title=title, description=description
    )
    iwas = container['all']

    # Set the Collection criteria.
    #: Sort on the Modification date
    iwas.sort_on = u'modified'
    iwas.sort_reversed = True
    iwas.relatedItems = ""
    #: Query by Type
    iwas.query = [
        {
            'i': u'dp_type',
            'o': u'plone.app.querystring.operation.selection.is',
            'v': [u'reireport'],
        },
        {
            u'i': u'review_state',
            u'o': u'plone.app.querystring.operation.selection.any',
            u'v': ['published', 'pending_bmu', 'pending_bfs', 'pending_authority', 'private'],
        },
    ]
    iwas.text = RichTextValue(
        '<p>Alle Reiberichte<p>',
        'text/html',
        'text/x-html-safe')

    iwas.setLayout('docpool_collection_view')

    print("Collection Alle angelegt")


def create_all_private_collection(plonesite):
    container = api.content.get(path='/berichte')

    title = 'noch nicht freigegeben'
    description = 'noch nicht freigegeben REI Berichte'
    _createObjectByType(
        'Collection', container, id='allprivate', title=title, description=description
    )
    iwas = container['allprivate']

    # Set the Collection criteria.
    #: Sort on the Modification date
    iwas.sort_on = u'modified'
    iwas.sort_reversed = True
    iwas.relatedItems = ""
    #: Query by Type and Review State
    iwas.query = [
        {
            'i': u'dp_type',
            'o': u'plone.app.querystring.operation.selection.is',
            'v': [u'reireport'],
        },
        {
            u'i': u'review_state',
            u'o': u'plone.app.querystring.operation.selection.any',
            u'v': ['pending_bfs', 'pending_bmu', 'pending_authority', 'private'],
        },
    ]
    iwas.text = RichTextValue(
        '<p>Noch freizugeben<p>',
        'text/html',
        'text/x-html-safe')

    iwas.setLayout('docpool_collection_view')

    print("Collection Alle eingereicht angelegt")


BASICSTRUCTURE = [
    {
        TYPE: 'Folder',
        TITLE: 'REI Berichte',
        ID: 'berichte',
        CHILDREN: [],  # TODO: further folders filled with REI Collections
    }
    # {
    #     TYPE: 'DPInfos', # when type is available
    #     TITLE: 'Infos',
    #     ID: 'rei-infos',
    #     CHILDREN: [
    #         {
    #             TYPE: 'InfoFolder',
    #             TITLE: 'Infos zu...',
    #             ID: 'info1'
    #         }
    #     ],
    # }
]

DTYPES = [
    {
        TYPE: 'DocType',
        TITLE: u'REI_Bericht',
        ID: 'reireport',
        CHILDREN: [],
        'local_behaviors': ['rei'],
    }
]
