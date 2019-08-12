# -*- coding: utf-8 -*-

from elan.sitrep.content.situationreport import ISituationReport
from elan.sitrep.content.srmodule import ISRModule
from five.grok import context
from five.grok import name
from plone.directives.dexterity.form import AddForm
from plone.directives.dexterity.form import EditForm


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
