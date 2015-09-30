# -*- coding: utf-8 -*-
#
# File: situationreport.py
#
# Copyright (c) 2015 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the SituationReport content type. See situationreport.py for more
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

from plone.dexterity.content import Container
from docpool.base.content.dpdocument import DPDocument, IDPDocument

from Products.CMFCore.utils import getToolByName

##code-section imports
##/code-section imports 

from elan.sitrep.config import PROJECTNAME

from elan.sitrep import ELAN_EMessageFactory as _

class ISituationReport(form.Schema, IDPDocument):
    """
    """
        
    phase = RelationChoice(
                        title=_(u'label_situationreport_phase', default=u'Phase (scenario-specific)'),
                        description=_(u'description_situationreport_phase', default=u''),
                        required=False,
##code-section field_phase
                        source = "elan.sitrep.vocabularies.Phases",
##/code-section field_phase                           
    )
    
        
    currentModules = RelationList(
                        title=_(u'label_situationreport_currentmodules', default=u'Current Modules'),
                        description=_(u'description_situationreport_currentmodules', default=u''),
                        required=False,
##code-section field_currentModules
                        value_type=RelationChoice(
                                                      title=_("Current Modules"),
                                                    source = "elan.sitrep.vocabularies.CurrentModules",

                                                     ),

##/code-section field_currentModules                           
    )
    

##code-section interface
    form.widget(phase='z3c.form.browser.select.SelectFieldWidget')
    form.widget(currentModules='z3c.form.browser.select.CollectionSelectFieldWidget')
    
    form.mode(docType='hidden')
    docType = schema.TextLine(
            title=u"Document Type",
            default=u"situationreport"
        )    
##/code-section interface


class SituationReport(Container, DPDocument):
    """
    """
    security = ClassSecurityInfo()
    
    implements(ISituationReport)
    
##code-section methods
    def customMenu(self, menu_items):
        """
        """
        return menu_items
    
    def myPhaseConfig(self):
        """
        """
        if self.phase:
            return self.phase.to_object
        else:
            return None
        
        
    def myModules(self):
        """
        """
        return [ m.to_object for m in (self.currentModules or [])]
            
##/code-section methods 

    def mySituationReport(self):
        """
        """
        return self

    def getFirstChild(self):
        """
        """
        fc = self.getFolderContents()
        if len(fc) > 0:
            return fc[0].getObject()
        else:
            return None

    def getAllContentObjects(self):
        """
        """
        return [obj.getObject() for obj in self.getFolderContents()]

    def getSRModules(self, **kwargs):
        """
        """
        args = {'portal_type':'SRModule'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 


##code-section bottom
##/code-section bottom 
