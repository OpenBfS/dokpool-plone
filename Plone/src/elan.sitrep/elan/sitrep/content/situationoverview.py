# -*- coding: utf-8 -*-
#
# File: situationoverview.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
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
from plone.namedfile.field import NamedBlobImage
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
##/code-section imports 

from elan.sitrep.config import PROJECTNAME

from elan.sitrep import DocpoolMessageFactory as _

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
        path = self.dpSearchPath()
        reports = queryForObjects(self, path=path, portal_type='SituationReport', sort_on='changed', sort_order='reverse', review_state='published', changed={
                 'query' : (DateTime() - 14).asdatetime().replace(tzinfo=None),
                 'range': 'min' },
                                  scenarios=uss
            )
        #mtypes = self.modTypes()
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
        default = [ ( "", _("Current situation") ) ]
        ud = [ ( "userdefined", _("User defined") ) ]
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
        return _availableModules(self, reportUID)
    
    def modinfo(self, moduid=None):
        """
        """
        if moduid:
            module = queryForObject(self, UID=moduid)
            if module:
                return module.restrictedTraverse("@@info")()
        return _("No content found")
            
##/code-section methods 


##code-section bottom
def _availableModules(self, reportUID=None):
    res = {}
    moduids = {}
    uss = getScenariosForCurrentUser(self)       
    path = self.dpSearchPath()
    
    for mt in self.modTypes():
            moduids[mt[0]] = None
            mods = queryForObjects(self, path=path, dp_type=mt[0], portal_type='SRModule', sort_on='changed', sort_order='reverse', 
                                   review_state='published', changed={
             'query' : (DateTime() - 14).asdatetime().replace(tzinfo=None),
             'range': 'min' },
                                   scenarios=uss
                                   )
            modres = [ (m.UID, "%s %s" % (m.Title, self.toLocalizedTime(DateTime(m.changed), long_format=1))) for m in mods]
            latest = mods and mods[0].changed or (DateTime() - 14).asdatetime().replace(tzinfo=None)
            if mods:
                moduids[mt[0]] = mods[0].UID
            current = queryForObjects(self, path=path, dp_type=mt[0], portal_type='SRModule', sort_on='changed', sort_order='reverse', 
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
    
##/code-section bottom 
