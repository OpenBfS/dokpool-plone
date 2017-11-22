# -*- coding: utf-8 -*-
from Products.CMFCore.utils import getToolByName
from docpool.config.utils import ID, TYPE, TITLE, CHILDREN, createPloneObjects, _addAllowedTypes
from docpool.base.events import IDocumentPoolUndeleteable
from Products.Five.utilities.marker import mark
from plone import api
import transaction

def install(plonesite):
    """
    """
    fresh = True
    if plonesite.hasObject("rodos"):
        fresh = False # It's a reinstall
    #configUsers(plonesite, fresh)
    createStructure(plonesite, fresh)

def configUsers(plonesite, fresh):
    """
    """
    if fresh:
        mtool = getToolByName(plonesite, "portal_membership")
        mtool.addMember('rodosadmin', 'RODOS Administrator (global)', ['Site Administrator', 'Member'], [])
        rodosadmin = mtool.getMemberById('rodosadmin')
        rodosadmin.setMemberProperties(
            {"fullname": 'RODOS Administrator'})
        rodosadmin.setSecurityProfile(password="admin")
        mtool.addMember('rodosmanager', 'RODOS Manager (global)', ['Manager', 'Member'], [])
        rodosmanager = mtool.getMemberById('rodosmanager')
        rodosmanager.setMemberProperties(
            {"fullname": 'RODOS Manager'})
        rodosmanager.setSecurityProfile(password="admin")
        # Role from rolemap.xml
        api.user.grant_roles(username='rodosmanager',  roles=['RodosUser'])
        api.user.grant_roles(username='rodosadmin', roles=['RodosUser'])
        api.user.grant_roles(username='dpmanager', roles=['RodosUser'])
        api.user.grant_roles(username='dpadmin', roles=['RodosUser'])


def createStructure(plonesite, fresh):
    createRodosNavigation(plonesite, fresh)
    transaction.commit()
    createRodosDocTypes(plonesite, fresh)
    transaction.commit()

def createRodosNavigation(plonesite, fresh):
    createPloneObjects(plonesite, BASICSTRUCTURE, fresh)

def createRodosDocTypes (plonesite, fresh):
    createPloneObjects(plonesite.config.dtypes, DTYPES, fresh)


BASICSTRUCTURE = [
    {
        TYPE: 'Folder',
        TITLE: 'RODOS Run Display',
        ID: 'rodos',
        CHILDREN: [
            {
                TYPE: 'Folder',
                TITLE: 'NPPs',
                ID: 'npps'
            }
        ], # TODO: further folders filled with RODOS Collections
    }
    # {
    #     TYPE: 'DPInfos', # when type is available
    #     TITLE: 'Infos',
    #     ID: 'rodos-infos',
    #     CHILDREN: [
    #         {
    #             TYPE: 'InfoFolder',
    #             TITLE: 'Infos zu...',
    #             ID: 'info1'
    #         }
    #     ],
    # }
]

DTYPES = [{TYPE: 'DocType', TITLE: u'RODOS Lauf', ID: 'rodos-run',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos'], 'allowedDocTypes' : [ 'rodos-plume-arrival' ]},
          {TYPE: 'DocType', TITLE: u'RODOS Ergebnis Wolkenankunftszeit', ID: 'rodos-plume-arrival',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
         ]