# -*- coding: utf-8 -*-
#
# File: situationreport.py
#
# Copyright (c) 2017 by Condat AG
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
from plone.namedfile.field import NamedBlobImage
from collective import dexteritytextindexer
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder
from Products.CMFPlone.utils import log, log_exc

from plone.dexterity.content import Container
from docpool.base.content.dpdocument import DPDocument, IDPDocument

from Products.CMFCore.utils import getToolByName

##code-section imports
from plone.api import content
from docpool.base.utils import portalMessage, queryForObject, back_references
from elan.sitrep.content.situationoverview import _availableModules
from datetime import datetime
import re
from plone.namedfile import NamedBlobFile 
from zope.interface import alsoProvides
from plone.protect.interfaces import IDisableCSRFProtection
from plone.dexterity.utils import safe_unicode
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from z3c.relationfield.relation import RelationValue
##/code-section imports 

from elan.sitrep.config import PROJECTNAME

from elan.sitrep import DocpoolMessageFactory as _

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
    text = RichText(
        title=_(u'label_situationreport_text', default=u'Introduction'),
        description=_(u'description_situationreport_text', default=u''),
        required=False
    )
    docType = schema.Choice(
        required=True,
        ##code-section field_docType
        source="docpool.base.vocabularies.DocumentTypes",
        default = u"sitrep",
        ##/code-section field_docType
    )

#    docType = schema.TextLine(
#            title=u"Document Type",
#            default=u"sitrep",
#    )

##/code-section interface


class SituationReport(Container, DPDocument):
    """
    """
    security = ClassSecurityInfo()
    
    implements(ISituationReport)
    
##code-section methods

    def typeName(self):
        return "sitrep"

    def dp_type(self):
        """
        """
        return "sitrep"

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
        copied_modules = self.getSRModules()
        if copied_modules: # should we ever use that
            return copied_modules
        else: # report under construction
            return [ m.to_object for m in (self.currentModules or [])]

    def modulesMeantForMe(self):
        """
        Alle modules linked to me but currently in process
        @return:
        """
        modules = back_references(self, "currentReport")
        return [ mod for mod in modules if mod is not None and mod.myState() == 'private' ]

    def publishedModulesMeantForMe(self):
        """
        Alle modules linked to me and published (but probably not yet assigned to me)
        @return:
        """
        modules = back_references(self, "currentReport")
        return [ mod for mod in modules if mod is not None and mod.myState() == 'published' ]


    def moduleState(self):
        """
        We need to collect all modules that are already published and assigned to this sitrep.
        Next we need those that are still in progress but are planned for this report.
        And lastly we determine alle module type for which there is no module whatsoever.
        @return:
        """
        # The "ready" modules.
        myMods = self.myModules()
        # The planned modules in progress.
        plannedMods = self.modulesMeantForMe()
        # The published modules in progress
        publishedMods = self.publishedModulesMeantForMe()
        mts = self.modTypes()
        missing = {}
        # As a start, all modules are missing
        for mt in mts:
            missing[mt[0]] = ['missing', mt[1], None]
        # Except for those in progress
        for mod in plannedMods:
            try:
                missing[mod.docType][0] = 'planned'
                missing[mod.docType][2] = mod
            except:
                pass

        for mod in publishedMods:
            try:
                missing[mod.docType][0] = 'published'
                missing[mod.docType][2] = mod
            except:
                pass

        # Even better: those ready
        for mod in myMods:
            try:
                missing[mod.docType][0] = 'ready'
                missing[mod.docType][2] = mod
            except:
                pass
        res = missing.values()
        #res = myMods
        #res.extend(plannedMods)
        return sorted(res)
            
    def publishReport(self, justDoIt=False, duplicate=False):
        """
        """
        request = self.REQUEST
        alsoProvides(request, IDisableCSRFProtection)
        new_version = self
        if duplicate:
            new_version = content.copy(source=self, id=self.getId(), safe_id=True)
        # copy modules into the report?
        # We would lose all the reference information, which is important for the situation overview
        #mods = self.myModules()
        #for mod in mods:
        #    content.copy(source=mod, target=new_version, safe_id=True)
        # create PDF, upload it
        data = self.restrictedTraverse("@@pdfprint")._generatePDF(raw=True)
        nice_filename = 'report_%s_%s.pdf' % (self.getId(), datetime.now().strftime('%Y%m%d'))
        nice_filename = safe_unicode(nice_filename)
        field = NamedBlobFile(data=data, filename=nice_filename)
        fid = new_version.invokeFactory(id=nice_filename, type_name="File", title=self.Title(), description="")
        f = new_version._getOb(fid)
        f.file = field
        f.reindexObject()
        
        content.transition(new_version, transition="publish")
        if not justDoIt:
            portalMessage(self, _("The report has been published."), "info")
            return self.restrictedTraverse("@@view")()
        
    def mirrorOverview(self):
        """
        """
        request = self.REQUEST
        alsoProvides(request, IDisableCSRFProtection)
        intids = getUtility(IIntIds)
        
        modules = _availableModules(self)
        modules = modules and modules[0] or {}
        # link to current modules
        refs = []
        for mt in self.modTypes():
            #print idx
            mod = modules.get(mt[0], None)
            if mod:
                #print mod
                try:
                    moduid = mod[0][0]
                    module = queryForObject(self, UID=moduid)
                    #print module
                    if module:
                        to_id = intids.getId(module)
                        refs.append(RelationValue(to_id))
                except:
                    pass
        if refs:
            self.currentModules = refs
            self.reindexObject()   
            portalMessage(self, _("Modules have been replaced with current situation overview."), "info")
        else:
            portalMessage(self, _("No modules found in current situation overview."), "warn")
        return self.restrictedTraverse("@@view")()
        
    def getRepresentativePDF(self):
        """
        """
        pdfPattern = "report.*\.pdf"
        p = re.compile(pdfPattern, re.IGNORECASE)
        files = self.getFiles()
        for f in files:
            if p.match(f.getId()):
                return f
        else:
            return None
        
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

    def getFiles(self, **kwargs):
        """
        """
        args = {'portal_type':'File'}
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
