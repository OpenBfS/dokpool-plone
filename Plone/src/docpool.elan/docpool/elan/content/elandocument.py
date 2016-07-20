# -*- coding: utf-8 -*-
#
# File: elandocument.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the ELANDocument content type. See elandocument.py for more
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
from docpool.base.content.documentextension import DocumentExtension, IDocumentExtension

from Products.CMFCore.utils import getToolByName

##code-section imports
from docpool.elan.config import ELAN_APP
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from plone import api
from docpool.base.content.doctype import IDocType
from docpool.transfers.config import TRANSFERS_APP
##/code-section imports 

from docpool.elan.config import PROJECTNAME

from docpool.elan import DocpoolMessageFactory as _

class IELANDocument(form.Schema, IDocumentExtension):
    """
    """

##code-section interface
    scenarios = schema.List(
        title=_(u'label_dpdocument_scenarios', default=u'Belongs to scenarios'),
        description=_(u'description_dpdocument_scenarios', default=u''),
        required=True,
        value_type=schema.Choice(source="elan.esd.vocabularies.Scenarios"),
    )

    form.widget(scenarios=CheckBoxFieldWidget)

@form.default_value(field=IELANDocument['scenarios'])
def initializeScenarios(data):
    if hasattr(data.context, "getUserSelectedScenarios"):
        return data.context.getUserSelectedScenarios()
    else:
        return []

##/code-section interface


class ELANDocument(Item, DocumentExtension):
    """
    """
    security = ClassSecurityInfo()
    
    implements(IELANDocument)
    
##code-section methods
    def myScenarioObjects(self):
        """
        """
        cat = getToolByName(self, "portal_catalog")
        scns = self.scenarios
        return [s.getObject() for s in cat(path=self.dpSearchPath(), portal_type='ELANScenario', getId=scns)]

    def scenarioIndex(self):
        """
        """
        scens = self.myScenarioObjects()
        res = [scen.getId() for scen in scens if api.content.get_state(scen) == u'published']
        return res

    def debugvalues(self):
        """
        """
        print self.scenarios
        print self.docType

    def getScenarioNames(self):
        """
        """
        cat = getToolByName(self, "portal_catalog")
        scns = self.scenarios
        return [s.Title for s in cat(path=self.dpSearchPath(), portal_type='ELANScenario', getId=scns)]

    def unknownScenario(self):
        """
        If my scenario is in state private, return it.
        """
        scns = self.myScenarioObjects()
        if scns:
            scn = scns[0]
            sstate = api.content.get_state(scn)
            if sstate == 'private':
                return scn
        return None

    def category(self):
        """
        """
        return self.typeAndCat()[1]

    def cat_path(self):
        """
        Catalog path for the category object. Needed for a patch to the getURL function of brains.
        """
        try:
            dto = self.docTypeObj()
            if dto:
                #                print "DTO"
                #                print dto.Title()
                cat = dto.doc_extension(ELAN_APP).contentCategory
                if cat:
                    aup = cat.to_path
                    #                    print aup
                    aup = "/".join(aup.split("/")[4:])
                    return aup
        except:
            return ""

    def typeAndCat(self):
        """
        """
        #        print self
        dto = self.docTypeObj()
        if dto:
            #            print dto
            if IDocType.providedBy(dto):
                return dto.title, dto.doc_extension(ELAN_APP).categories()
            else:
                return dto.title, []
        else:
            return ("", [])
##/code-section methods 


##code-section bottom
##/code-section bottom 
