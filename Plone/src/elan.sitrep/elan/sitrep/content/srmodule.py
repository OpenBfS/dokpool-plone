# -*- coding: utf-8 -*-
#
# File: srmodule.py
#
# Copyright (c) 2015 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the SRModule content type. See srmodule.py for more
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

class ISRModule(form.Schema, IDPDocument):
    """
    """
        
    currentReport = RelationChoice(
                        title=_(u'label_srmodule_currentreport', default=u'Current report'),
                        description=_(u'description_srmodule_currentreport', default=u'If selected this report defines helpful defaults (text blocks, documents) for the content of this module.'),
                        required=False,
##code-section field_currentReport
                        source = "elan.sitrep.vocabularies.CurrentReports",
##/code-section field_currentReport                           
    )
    

##code-section interface
# Change vocab for docTypes to moduleTypes # TODO:
    docType = schema.Choice(
                        title=_(u'label_srmodule_doctype', default=u'Module Type'),
                        description=_(u'description_srmodule_doctype', default=u''),
                        required=True,
                        source="elan.sitrep.vocabularies.ModuleTypes",
    )
    form.widget(currentReport='z3c.form.browser.select.SelectFieldWidget')

##/code-section interface


class SRModule(Container, DPDocument):
    """
    """
    security = ClassSecurityInfo()
    
    implements(ISRModule)
    
##code-section methods
    def customMenu(self, menu_items):
        """
        """
        return menu_items
    
    def getModuleTitle(self):
        """
        """
        if self.currentReport:
            return "%s: %s" % (self.currentReport.to_object.Title(), self.Title())
        else:
            return self.Title()
##/code-section methods 

    def mySRModule(self):
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
