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
    if plonesite.hasObject("rei"):
        fresh = False # It's a reinstall
    #configUsers(plonesite, fresh)
    createStructure(plonesite, fresh)

def configUsers(plonesite, fresh):
    """
    """
    if fresh:
        mtool = getToolByName(plonesite, "portal_membership")
        mtool.addMember('reiadmin', 'REI Administrator (global)', ['Site Administrator', 'Member'], [])
        reiadmin = mtool.getMemberById('reiadmin')
        reiadmin.setMemberProperties(
            {"fullname": 'REI Administrator'})
        reiadmin.setSecurityProfile(password="admin")
        mtool.addMember('reimanager', 'REI Manager (global)', ['Manager', 'Member'], [])
        reimanager = mtool.getMemberById('reimanager')
        reimanager.setMemberProperties(
            {"fullname": 'REI Manager'})
        reimanager.setSecurityProfile(password="admin")
        # Role from rolemap.xml
        api.user.grant_roles(username='reimanager',  roles=['REIUser'])
        api.user.grant_roles(username='reiadmin', roles=['REIUser'])
        api.user.grant_roles(username='dpmanager', roles=['REIUser'])
        api.user.grant_roles(username='dpadmin', roles=['REIUser'])


def createStructure(plonesite, fresh):
    createREINavigation(plonesite, fresh)
    transaction.commit()
    createREIDocTypes(plonesite, fresh)
    transaction.commit()

def createREINavigation(plonesite, fresh):
    createPloneObjects(plonesite, BASICSTRUCTURE, fresh)
    print "struktur angelegt"

def createREIDocTypes (plonesite, fresh):
    createPloneObjects(plonesite.config.dtypes, DTYPES, fresh)
    print "REI Bericht angelegt"

BASICSTRUCTURE = [
    {
        TYPE: 'Folder',
        TITLE: 'REI Berichte',
        ID: 'berichte',
        CHILDREN: [


        ], # TODO: further folders filled with REI Collections
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


          {TYPE: 'DocType', TITLE: u'REI_Bericht', ID: 'reireport',
           CHILDREN: [], 'local_behaviors' : ['rei']},
         ]

