# -*- coding: utf-8 -*-
#
# File: srmodule.py
#
# Copyright (c) 2016 by Condat AG
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
from plone.namedfile.field import NamedBlobImage
from collective import dexteritytextindexer
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder
from Products.CMFPlone.utils import log, log_exc

from plone.dexterity.content import Container
from docpool.base.content.dpdocument import DPDocument, IDPDocument

from Products.CMFCore.utils import getToolByName

##code-section imports
from docpool.base.utils import queryForObjects, back_references, portalMessage
from plone.api import content
from elan.sitrep.vocabularies import ModuleTypesVocabularyFactory
from DateTime import DateTime
from zope.interface import alsoProvides
from plone.protect.interfaces import IDisableCSRFProtection
from plone.app.textfield.value import RichTextValue
##/code-section imports 

from elan.sitrep.config import PROJECTNAME

from elan.sitrep import DocpoolMessageFactory as _

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
    def createActions(self):
        super(DPDocument, self).createActions()
        self.text = RichTextValue(_(u"No information."), 'text/plain', 'text/html')

    def customMenu(self, menu_items):
        """
        """
        return menu_items
    
    def getModuleTitle(self):
        """
        """
        if self.currentReport:
            return "%s: %s (%s)" % (self.currentReport.to_object.Title(), self.Title(), self.toLocalizedTime(DateTime(self.changed()), long_format=1))
        else:
            return self.Title()
    
    def myReport(self):
        """
        """
        if self.currentReport:
            return self.currentReport.to_object
        else:
            return None
        
    def previousVersions(self):
        """
        """
        path = self.dpSearchPath()
        brains = queryForObjects(self, path=path, portal_type='SRModule', dp_type=self.docType,review_state='published', sort_on='changed', sort_order='reverse')        
        return brains
    
    def previousVersion(self):
        """
        The previous version is the instance youngest published instance of SRModule with the same Module Type.
        """
        pv = self.previousVersions()
        if len(pv) > 0:
            return pv[0].getObject()
        else:
            return None
        
    def defaultFilter(self):
        """
        Determines all default filter criteria for text blocks by looking at the currentReport and module type.
        """
        modType = self.docType
        res = { 'scenario' : None,
                'phase' : None,
                'module_type' : modType,
                'mandatory' : False,
                'config' : None }
        r = self.myReport()
        if r:
            p = r.myPhaseConfig()
            if p:
                res['phase'] = p.getId()
                res['scenario'] = p.mySRScenario().getId()
                # my module is mandatory if the designated phase has a moduleconfig for my type
                mcs = p.availableModuleConfigs()
                if mcs.get(modType, None):
                    res['mandatory'] = True
                    res['config'] = mcs.get(modType, None)
        return res
    
    def getFilter(self, request):
        """
        """
        df = self.defaultFilter()
        scenario = request.get('scenario', df['scenario'])
        phase = request.get('phase', df['phase'])
        module_type = request.get('module_type', df['module_type'])
        return scenario, phase, module_type
    
    def possibleSRScenarios(self):
        """
        """
        path = self.dpSearchPath()
        return [ ( "", '---') ] + [ ( brain.getId, brain.Title) for brain in queryForObjects(self, path=path, portal_type='SRScenario', sort_on='sortable_title') ]

    def possibleSRPhases(self):
        """
        """
        path = self.dpSearchPath()
        raw = queryForObjects(self, path=path, portal_type='SRPhase', sort_on='sortable_title')
        ids = []
        res = []
        for p in raw:
            if p.getId in ids:
                continue
            else:
                ids.append(p.getId)
                res.append(p)
        return [ ( "", '---') ] + [ ( brain.getId, brain.Title) for brain in res ]
        
    def possibleSRModuleTypes(self):
        """
        """
        return [ ( "", '---') ] + ModuleTypesVocabularyFactory(self, raw=True)

    def usingReports(self):
        """
        Which reports am I being used in?
        """
        reports = back_references(self, "currentModules")
        return reports
    
    def visualisations(self):
        """
        """
        df = self.defaultFilter()
        mc = df['config']
        res = []
        if mc:
            res = mc.currentDocuments()[:20]
        if not res:
            mt = self.docTypeObj()
            if mt:
                res = mt.currentDocuments()[:20]
        return res 
        
    def textBlocks(self):
        """
        """
        request = self.REQUEST
        path = self.dpSearchPath()
        scenario, phase, module_type = None, None, None
        if request.get('filtered', False):
            scenario, phase, module_type = self.getFilter(request)
        else:
            df = self.defaultFilter()
            mc = df['config']
            if mc:
                return mc.currentTextBlocks()
        args = {'portal_type':'SRTextBlock', 'sort_on':'sortable_title', 'path': path }
        if scenario:
            args['scenarios'] = scenario
        if phase:
            args['phases'] = phase
        if module_type:
            args['modules'] = module_type
        #print args
        sr_cat = getToolByName(self, 'sr_catalog')
        if scenario or phase or module_type:
            return [ brain.getObject() for brain in sr_cat(**args) ]
        else:
            return []
        
    def publishModule(self, justDoIt=False):
        """
        """
        request = self.REQUEST
        alsoProvides(request, IDisableCSRFProtection)        

        new_version = content.copy(source=self, id=self.getId(), safe_id=True)
        content.transition(new_version, transition="publish")
        if not justDoIt:
            portalMessage(self, _("The module has been published."), "info")
            return self.restrictedTraverse("@@view")()
        

    def docTypeObj(self):
        mt = self.dp_type()
        if not mt: # The object is just being initialized and the attributes have not yet been saved
            mt = self.REQUEST.get('docType','')
        #dto = queryForObject(self, id=et)
        dto = None
#        print mt
        try:
            dto = self.config.mtypes[mt]
        except Exception, e:
            # et can be empty
            print e
            pass
        if not dto:
            log("No ModuleType Object for type name '%s'" % self.dp_type())
        return dto
    
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

    def getELANDocuments(self, **kwargs):
        """
        """
        args = {'portal_type':'ELANDocument'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 

    def getSRModules(self, **kwargs):
        """
        """
        args = {'portal_type':'SRModule'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 

    def getTransferables(self, **kwargs):
        """
        """
        args = {'portal_type':'Transferable'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 


##code-section bottom
##/code-section bottom 
