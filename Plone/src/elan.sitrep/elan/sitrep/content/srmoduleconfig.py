# -*- coding: utf-8 -*-
#
# File: srmoduleconfig.py
#
# Copyright (c) 2015 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the SRModuleConfig content type. See srmoduleconfig.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from zope.interface import implements
from zope.component import adapts
from zope import schema
from plone.directives import form, dexterity
from plone.app.textfield import RichText
from collective import dexteritytextindexer
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder
from Products.CMFPlone.utils import log, log_exc

from plone.dexterity.content import Item

from Products.CMFCore.utils import getToolByName

##code-section imports
from zope.component import adapter
from plone.dexterity.interfaces import IEditFinishedEvent
##/code-section imports 

from elan.sitrep.config import PROJECTNAME

from elan.sitrep import ELAN_EMessageFactory as _

class ISRModuleConfig(form.Schema):
    """
    """
        
    modType = schema.Choice(
                        title=_(u'label_srmoduleconfig_modtype', default=u'Module Type'),
                        description=_(u'description_srmoduleconfig_modtype', default=u''),
                        required=True,
##code-section field_modType
                        source="elan.sitrep.vocabularies.ModuleTypes",
##/code-section field_modType                           
    )
    
        
    docSelection = RelationChoice(
                        title=_(u'label_srmoduleconfig_docselection', default=u'Collection for relevant documents'),
                        description=_(u'description_srmoduleconfig_docselection', default=u'This collection defines a pre-selection of possible documents to reference within this module.'),
                        required=False,
##code-section field_docSelection
                        source = "elan.sitrep.vocabularies.Collections",
##/code-section field_docSelection                           
    )
    
        
    textBlocks = RelationList(
                        title=_(u'label_srmoduleconfig_textblocks', default=u'Text Blocks'),
                        description=_(u'description_srmoduleconfig_textblocks', default=u''),
                        required=False,
##code-section field_textBlocks
                        value_type=RelationChoice(
                                                      title=_("Text Blocks"),
                                                      source = "elan.sitrep.vocabularies.TextBlocks",

                                                     ),
##/code-section field_textBlocks                           
    )
    

##code-section interface
    form.widget(docSelection='z3c.form.browser.select.SelectFieldWidget')
    form.widget(textBlocks='z3c.form.browser.select.CollectionSelectFieldWidget')
##/code-section interface


class SRModuleConfig(Item):
    """
    """
    security = ClassSecurityInfo()
    
    implements(ISRModuleConfig)
    
##code-section methods
    def getSRModuleNames(self):
        """
        Index Method
        """
        return [ self.modType ]

    def getSRModuleRefs(self):
        """
        Index Method
        """
        return [ self.UID() ]
##/code-section methods 


##code-section bottom
@adapter(ISRModuleConfig, IEditFinishedEvent)
def updated(obj, event=None):
    log("SRModuleConfig updated: %s" % str(obj))
    sr_cat = getToolByName(obj, "sr_catalog")
    sr_cat.reindexObject(obj)
    for tb in obj.textBlocks:
        sr_cat.reindexObject(tb.to_object)

##/code-section bottom 
