# -*- coding: utf-8 -*-

from plone.directives.dexterity.form import EditForm, AddForm
from five.grok import context, name
from z3c.form import button
from docpool.base import DocpoolMessageFactory as _
from Products.CMFPlone import PloneMessageFactory as PMF
from Products.Archetypes.utils import shasattr
from elan.sitrep.content.situationreport import ISituationReport
from elan.sitrep.content.srmodule import ISRModule
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class SituationReportEditForm(EditForm):
    context(ISituationReport)
    
        
class SituationReportAddForm(AddForm):
    name('SituationReport')

class SRModuleEditForm(EditForm):
    context(ISRModule)
                
class SRModuleAddForm(AddForm):
    name('SRModule')
 
    def updateWidgets(self):
        super(SRModuleAddForm, self).updateWidgets()
        del self.widgets['text']
     
