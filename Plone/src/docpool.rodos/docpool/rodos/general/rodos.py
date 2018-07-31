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

DTYPES = [

          {TYPE: 'DocType', TITLE: u'RODOS Lauf', ID: 'rodos_run',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos'], 'ref_allowedDocTypes' : [ 'rodos_plume-arrival_close', 'rodos_plume-arrival_country', 'rodos_plume-arrival_whole', 'rodos_plumedeparture_close', 'rodos_plumedeparture_country', 'rodos_plumedeparture_whole', 'rodos_leafyvegetables_caesium_close', 'rodos_leafyvegetables_caesium_country', 'rodos_leafyvegetables_caesium_whole', 'rodos_leafyvegetables_iodine_close', 'rodos_leafyvegetables_iodine_country', 'rodos_leafyvegetables_iodine_whole', 'rodos_cowmilk_caesium_close', 'rodos_cowmilk_caesium_country', 'rodos_cowmilk_caesium_whole', 'rodos_cowmilk_iodine_close', 'rodos_cowmilk_iodine_country', 'rodos_cowmilk_iodine_whole', 'rodos_cowmilk_caesium_close', 'rodos_cowmilk_caesium_country', 'rodos_cowmilk_caesium_whole', 'rodos_effectivedose_7d_adults_close', 'rodos_effectivedose_7d_adults_country', 'rodos_effectivedose_7d_adults_whole', 'rodos_effectivedose_7d_children_close', 'rodos_effectivedose_7d_children_country', 'rodos_effectivedose_7d_children_whole', 'rodos_thyroiddose_7d_adults_close', 'rodos_thyroiddose_7d_adults_country', 'rodos_thyroiddose_7d_adults_whole', 'rodos_tyhroiddose_7d_children_close', 'rodos_tyhroiddose_7d_children_country', 'rodos_tyhroiddose_7d_children_whole', 'rodos_effectivedose_1y_adults_close', 'rodos_effectivedose_1y_adults_country', 'rodos_effectivedose_1y_adults_whole', 'rodos_gammadoserate_close', 'rodos_gammadoserate_country', 'rodos_gammadoserate_whole',]},
          {TYPE: 'DocType', TITLE: u'RODOS_pot_betr_Gebiete', ID: 'rodos_potaffectedareas',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_W-Ankunft_nah', ID: 'rodos_plumearrival_close',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_W-Ankunft_D', ID: 'rodos_plumearrival_country',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_W-Ankunft_ges', ID: 'rodos_plumearrival_whole',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_W-Abzug_nah', ID: 'rodos_plumedeparture_close',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_W-Abzug_D', ID: 'rodos_plumedeparture_country',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_W-Abzug_ges', ID: 'rodos_plumedeparture_whole',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_Blgem_Cs_nah', ID: 'rodos_leafyvegetables_caesium_close',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_Blgem_Cs_D', ID: 'rodos_leafyvegetables_caesium_country',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_Blgem_Cs_ges', ID: 'rodos_leafyvegetables_caesium_whole',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_Blgem_I_nah', ID: 'rodos_leafyvegetables_iodine_close',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_Blgem_I_D', ID: 'rodos_leafyvegetables_iodine_country',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_Blgem_I_ges', ID: 'rodos_leafyvegetables_iodine_whole',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_Kuhmilch_Cs_nah', ID: 'rodos_cowmilk_caesium_close',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_Kuhmilch_Cs_D', ID: 'rodos_cowmilk_caesium_country',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_Kuhmilch_Cs_ges', ID: 'rodos_cowmilk_caesium_whole',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_Kuhmilch_I_nah', ID: 'rodos_cowmilk_iodine_close',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_Kuhmilch_I_D', ID: 'rodos_cowmilk_iodine_country',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_Kuhmilch_I_ges', ID: 'rodos_cowmilk_iodine_whole',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_ED_7d_Erw_nah', ID: 'rodos_effectivedose_7d_adults_close',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_ED_7d_Erw_D', ID: 'rodos_effectivedose_7d_adults_country',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_ED_7d_Erw_ges', ID: 'rodos_effectivedose_7d_adults_whole',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_ED_7d_Ki_nah', ID: 'rodos_effectivedose_7d_children_close',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_ED_7d_Ki_D', ID: 'rodos_effectivedose_7d_children_country',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_ED_7d_Ki_ges', ID: 'rodos_effectivedose_7d_children_whole',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_Schild_7d_Erw_nah', ID: 'rodos_thyroiddose_7d_adults_close',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_Schild_7d_Erw_D', ID: 'rodos_thyroiddose_7d_adults_country',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_Schild_7d_Erw_ges', ID: 'rodos_thyroiddose_7d_adults_whole',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_Schild_7d_Ki_nah', ID: 'rodos_tyhroiddose_7d_children_close',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_Schild_7d_Ki_D', ID: 'rodos_thyroiddose_7d_children_country',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_Schild_7d_Ki_ges', ID: 'rodos_thyroiddose_7d_children_whole',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_ED_1J_Erw_nah', ID: 'rodos_effectivedose_1y_adults_close',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_ED_1J_Erw_D', ID: 'rodos_effectivedose_1y_adults_country',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_ED_1J_Erw_ges', ID: 'rodos_effectivedose_1y_adults_whole',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_GDRate_nah', ID: 'rodos_gammadoserate_close',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_GDRate_D', ID: 'rodos_gammadoserate_country',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
          {TYPE: 'DocType', TITLE: u'RODOS_GDRate_ges', ID: 'rodos_gammadoserate_whole',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rodos']},
         ]

