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

def createREIDocTypes (plonesite, fresh):
    createPloneObjects(plonesite.config.dtypes, DTYPES, fresh)


BASICSTRUCTURE = [
    {
        TYPE: 'Folder',
        TITLE: 'REI Run Display',
        ID: 'rei',
        CHILDREN: [
            {
                TYPE: 'Folder',
                TITLE: 'NPPs',
                ID: 'npps'
            }
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

          {TYPE: 'DocType', TITLE: u'REI Lauf', ID: 'rei_run',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei'], 'ref_allowedDocTypes' : [ 'rei_zip', 'rei_plume-arrival_close', 'rei_plume-arrival_country', 'rei_plume-arrival_whole', 'rei_plumearrival_zip', 'rei_plumedeparture_close', 'rei_plumedeparture_country', 'rei_plumedeparture_whole', 'rei_plumedeparture_zip', 'rei_leafyvegetables_caesium_close', 'rei_leafyvegetables_caesium_country', 'rei_leafyvegetables_caesium_whole', 'rei_ban_on_selling_leafyvegetables_cs_zip', 'rei_leafyvegetables_iodine_close', 'rei_leafyvegetables_iodine_country', 'rei_leafyvegetables_iodine_whole', 'rei_ban_on_selling_leafyvegetables_i_zip', 'rei_cowmilk_caesium_close', 'rei_cowmilk_caesium_country', 'rei_cowmilk_caesium_whole', 'rei_ban_on_selling_cowmilk_cs_zip', 'rei_cowmilk_iodine_close', 'rei_cowmilk_iodine_country', 'rei_cowmilk_iodine_whole', 'rei_ban_on_selling_cowmilk_iodine_zip', 'rei_groundcontamination_i131_close', 'rei_groundcontamination_i131_country', 'rei_groundcontamination_i131_whole', 'rei_groundcontamination_cs137_close', 'rei_groundcontamination_cs137_country', 'rei_groundcontamination_cs137_whole', 'rei_timeintegrated_airactivity_xe133_close', 'rei_timeintegrated_airactivity_xe133_country', 'rei_timeintegrated_airactivity_xe133_whole', 'rei_effectivedose_7d_adults_close', 'rei_effectivedose_7d_adults_country', 'rei_effectivedose_7d_adults_whole', 'rei_evacuation_sheltering_adults_zip', 'rei_effectivedose_7d_children_close', 'rei_effectivedose_7d_children_country', 'rei_effectivedose_7d_children_whole', 'rei_evacuation_sheltering_children_zip','rei_thyroiddose_7d_adults_close', 'rei_thyroiddose_7d_adults_country', 'rei_thyroiddose_7d_adults_whole', 'rei_iodinetablets_adults_zip', 'rei_tyhroiddose_7d_children_close', 'rei_tyhroiddose_7d_children_country', 'rei_tyhroiddose_7d_children_whole', 'rei_iodinetablets_children_zip', 'rei_effectivedose_1y_adults_close', 'rei_effectivedose_1y_adults_country', 'rei_effectivedose_1y_adults_whole', 'rei_evacuation_sheltering_adults_1y_zip', 'rei_gammadoserate_close', 'rei_gammadoserate_country', 'rei_gammadoserate_whole', 'rei_gdr_zip', 'rei_sourceterm_user', 'rei_sourceterm_detailed',]},
          {TYPE: 'DocType', TITLE: u'REI_pot_betr_Gebiete', ID: 'rei_potaffectedareas',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_zip', ID: 'rei_zip',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_W-Ankunft_nah', ID: 'rei_plumearrival_close',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_W-Ankunft_D', ID: 'rei_plumearrival_country',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_W-Ankunft_ges', ID: 'rei_plumearrival_whole',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_W-Ankunft_zip', ID: 'rei_plumearrival_zip',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_W-Abzug_nah', ID: 'rei_plumedeparture_close',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_W-Abzug_D', ID: 'rei_plumedeparture_country',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_W-Abzug_ges', ID: 'rei_plumedeparture_whole',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_W-Abzug_zip', ID: 'rei_plumedeparture_zip',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_Blgem_Cs_nah', ID: 'rei_leafyvegetables_caesium_close',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_Blgem_Cs_D', ID: 'rei_leafyvegetables_caesium_country',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_Blgem_Cs_ges', ID: 'rei_leafyvegetables_caesium_whole',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_Vermsperre_Blattgem_Cs_zip', ID: 'rei_ban_on_selling_leafyvegetables_cs_zip',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_Blgem_I_nah', ID: 'rei_leafyvegetables_iodine_close',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_Blgem_I_D', ID: 'rei_leafyvegetables_iodine_country',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_Blgem_I_ges', ID: 'rei_leafyvegetables_iodine_whole',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_Vermsperre_Blattgem_I_zip', ID: 'rei_ban_on_selling_leafyvegetables_i_zip',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_Kuhmilch_Cs_nah', ID: 'rei_cowmilk_caesium_close',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_Kuhmilch_Cs_D', ID: 'rei_cowmilk_caesium_country',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_Kuhmilch_Cs_ges', ID: 'rei_cowmilk_caesium_whole',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_Vermsperre_Milch_Cs_zip', ID: 'rei_ban_on_selling_cowmilk_cs_zip',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},

          {TYPE: 'DocType', TITLE: u'REI_Kuhmilch_I_nah', ID: 'rei_cowmilk_iodine_close',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_Kuhmilch_I_D', ID: 'rei_cowmilk_iodine_country',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_Kuhmilch_I_ges', ID: 'rei_cowmilk_iodine_whole',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_Vermsperre_Milch_I_zip', ID: 'rei_ban_on_selling_cowmilk_i_zip',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},

          {TYPE: 'DocType', TITLE: u'REI_Oberflkont_I131_nah', ID: 'rei_groundcontamination_i131_close',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_Oberflkont_I131_D', ID: 'rei_groundcontamination_i131_country',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_Oberflkont_I131_ges', ID: 'rei_groundcontamination_i131_whole',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_Oberflkont_Cs137_nah', ID: 'rei_groundcontamination_cs137_close',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_Oberflkont_Cs137_D', ID: 'rei_groundcontamination_cs137_country',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_Oberflkont_Cs137_ges', ID: 'rei_groundcontamination_cs137_whole',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_zeitintegr_Luftakt_Xe133_nah', ID: 'rei_timeintegrated_airactivity_xe133_close',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_zeitintegr_Luftakt_Xe133_D', ID: 'rei_timeintegrated_airactivity_xe133_country',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_zeitintegr_Luftakt_Xe133_ges', ID: 'rei_timeintegrated_airactivity_xe133_whole',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_ED_7d_Erw_nah', ID: 'rei_effectivedose_7d_adults_close',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_ED_7d_Erw_D', ID: 'rei_effectivedose_7d_adults_country',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_ED_7d_Erw_ges', ID: 'rei_effectivedose_7d_adults_whole',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_Evak_Verbl_Erw_zip', ID: 'rei_evacuation_sheltering_adults_zip',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_ED_7d_Ki_nah', ID: 'rei_effectivedose_7d_children_close',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_ED_7d_Ki_D', ID: 'rei_effectivedose_7d_children_country',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_ED_7d_Ki_ges', ID: 'rei_effectivedose_7d_children_whole',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_Evak_Verbl_Ki_zip', ID: 'rei_evacuation_sheltering_children_zip',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_Schild_7d_Erw_nah', ID: 'rei_thyroiddose_7d_adults_close',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_Schild_7d_Erw_D', ID: 'rei_thyroiddose_7d_adults_country',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_Schild_7d_Erw_ges', ID: 'rei_thyroiddose_7d_adults_whole',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_Iodtabl_Erw_zip', ID: 'rei_iodinetablets_adults_zip',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_Schild_7d_Ki_nah', ID: 'rei_tyhroiddose_7d_children_close',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_Schild_7d_Ki_D', ID: 'rei_thyroiddose_7d_children_country',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_Schild_7d_Ki_ges', ID: 'rei_thyroiddose_7d_children_whole',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_Iodtabl_Ki_zip', ID: 'rei_iodinetablets_children_zip',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_ED_1J_Erw_nah', ID: 'rei_effectivedose_1y_adults_close',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_ED_1J_Erw_D', ID: 'rei_effectivedose_1y_adults_country',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_ED_1J_Erw_ges', ID: 'rei_effectivedose_1y_adults_whole',
          CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_Evak_Verbl_Erw_1J_zip', ID: 'rei_evacuation_sheltering_adults_1y_zip',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_GammaODL_nah', ID: 'rei_gammadoserate_close',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_GammaODL_D', ID: 'rei_gammadoserate_country',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_GammaODL_ges', ID: 'rei_gammadoserate_whole',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_ODL_zip', ID: 'rei_gdr_zip',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_Quellterm_Nutzereingabe', ID: 'rei_sourceterm_user',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
          {TYPE: 'DocType', TITLE: u'REI_Quellterm_detailliert', ID: 'rei_sourceterm_detailed',
           CHILDREN: [], 'local_behaviors' : ['elan', 'rei']},
         ]

