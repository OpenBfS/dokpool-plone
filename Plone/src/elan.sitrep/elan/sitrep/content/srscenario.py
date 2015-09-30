# -*- coding: utf-8 -*-
#
# File: srscenario.py
#
# Copyright (c) 2015 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the SRScenario content type. See srscenario.py for more
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

from Products.CMFCore.utils import getToolByName

##code-section imports
from zope.component import adapter
from plone.dexterity.interfaces import IEditFinishedEvent
from elan.sitrep.vocabularies import ModuleTypesVocabularyFactory
##/code-section imports 

from elan.sitrep.config import PROJECTNAME

from elan.sitrep import ELAN_EMessageFactory as _

class ISRScenario(form.Schema):
    """
    """

##code-section interface
##/code-section interface


class SRScenario(Container):
    """
    """
    security = ClassSecurityInfo()
    
    implements(ISRScenario)
    
##code-section methods
    def getSRScenarioNames(self):
        """
        Index Method
        """
        return [ self.getId() ]

    def getSRScenarioRefs(self):
        """
        Index Method
        """
        return [ self.UID() ]

    def modTypes(self):
        """
        """
        return ModuleTypesVocabularyFactory(self, raw=True)
    
    def modTypeIds(self):
        mtypes = self.modTypes()
        return [ mt[0] for mt in mtypes ]
    
    def getSRScenarios(self):
        """
        """
        return [ self ]

##/code-section methods 

    def mySRScenario(self):
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

    def getSRPhases(self, **kwargs):
        """
        """
        args = {'portal_type':'SRPhase'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 


##code-section bottom
@adapter(ISRScenario, IEditFinishedEvent)
def updated(obj, event=None):
    log("SRScenario updated: %s" % str(obj))
    sr_cat = getToolByName(obj, "sr_catalog")
    sr_cat.reindexObject(obj)
##/code-section bottom 
