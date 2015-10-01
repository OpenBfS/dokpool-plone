# -*- coding: utf-8 -*-
#
# File: situationoverview.py
#
# Copyright (c) 2015 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the SituationOverview content type. See situationoverview.py for more
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
from docpool.base.utils import queryForObjects, queryForObject
from DateTime import DateTime
from elan.sitrep.vocabularies import ModuleTypesVocabularyFactory
from elan.esd.utils import getScenariosForCurrentUser
from Products.CMFPlone.i18nl10n import utranslate
##/code-section imports 

from elan.sitrep.config import PROJECTNAME

from elan.sitrep import ELAN_EMessageFactory as _

class ISituationOverview(form.Schema):
    """
    """

##code-section interface
##/code-section interface


class SituationOverview(Item):
    """
    """
    security = ClassSecurityInfo()
    
    implements(ISituationOverview)
    
##code-section methods
    def srConfig(self):
        pass # TODO:
    

    def modTypes(self):
        """
        """
        return ModuleTypesVocabularyFactory(self, raw=True)
    
    
    def availableSituationReports(self):
        """
        For every situation report:
        * Get all modules that belong to it
        * Determine "missing" modules
        """
        uss = getScenariosForCurrentUser(self)
        reports = queryForObjects(self, portal_type='SituationReport', sort_on='changed', sort_order='reverse', review_state='published', changed={
                 'query' : (DateTime() - 14).asdatetime().replace(tzinfo=None),
                 'range': 'min' },
                                  scenarios=uss
            )
        mtypes = self.modTypes()
        res1 = []
        res2 = {}
        for report in [ r.getObject() for r in reports]:
            #mods = {}
            #for mt in mtypes:
            #    mods[mt[0]] = None
            #ms = report.myModules()
            #for m in ms:
            #    mods[m.docType] = m
            #res2[report.UID()] = ( report, mods )
            res1.append((report.UID(), "%s %s" % (report.Title(), self.toLocalizedTime(DateTime(report.changed()), long_format=1))))
        default = [ ( "", utranslate("elan.sitrep", "Current situation", context=self) ) ]
        ud = [ ( "userdefined", utranslate("elan.sitrep", "User defined", context=self) ) ]
        return default + res1 + ud, res2
                    
    def availableModules(self, reportUID=None):
        """
        For every module type:
        * Get all published modules (back two weeks)
        * Only for the currently selected events.
        * Check if there is a private version of the module newer that the latest published version.
        * Optional: check if that version is currently locked.
        If reportUID is given, determine the UIDs for that report's modules, otherwise determine the UID of the
        most recent module for each type.
        """
        res = {}
        moduids = {}
        uss = getScenariosForCurrentUser(self)        
        for mt in self.modTypes():
                moduids[mt[0]] = None
                mods = queryForObjects(self, dp_type=mt[0], portal_type='SRModule', sort_on='changed', sort_order='reverse', 
                                       review_state='published', changed={
                 'query' : (DateTime() - 14).asdatetime().replace(tzinfo=None),
                 'range': 'min' },
                                       scenarios=uss
                                       )
                modres = [ (m.UID, "%s %s" % (m.Title, self.toLocalizedTime(DateTime(m.changed), long_format=1))) for m in mods]
                latest = mods and mods[0].changed or (DateTime() - 14).asdatetime().replace(tzinfo=None)
                if mods:
                    moduids[mt[0]] = mods[0].UID
                current = queryForObjects(self, dp_type=mt[0], portal_type='SRModule', sort_on='changed', sort_order='reverse', 
                                       review_state='private', changed={
                 'query' : latest,
                 'range': 'min' },
                                       scenarios=uss
                                       )
                if current:
                    current = current[0].getObject()
                else:
                    current = None
                res[mt[0]] = ( modres, current )
        if reportUID:
            report = queryForObject(self, UID=reportUID)
            if report:
                ms = report.myModules()
                for m in ms:
                    moduids[m.docType] = m.UID()                
        return res, moduids
        
    def modinfo(self, moduid=None):
        """
        """
        if moduid:
            module = queryForObject(self, UID=moduid)
            if module:
                return module.restrictedTraverse("@@info")()
        return utranslate("elan.sitrep", "No content found", context=self)
            
##/code-section methods 


##code-section bottom
##/code-section bottom 
