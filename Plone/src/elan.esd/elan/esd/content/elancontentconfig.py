# -*- coding: utf-8 -*-
#
# File: elancontentconfig.py
#
# Copyright (c) 2015 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the ELANContentConfig content type. See elancontentconfig.py for more
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
##/code-section imports 

from elan.esd.config import PROJECTNAME

from elan.esd import ELAN_EMessageFactory as _

class IELANContentConfig(form.Schema):
    """
    """

##code-section interface
##/code-section interface


class ELANContentConfig(Container):
    """
    """
    security = ClassSecurityInfo()
    
    implements(IELANContentConfig)
    
##code-section methods
##/code-section methods 

    def myELANContentConfig(self):
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

    def getELANScenarioss(self, **kwargs):
        """
        """
        args = {'portal_type':'ELANScenarios'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 

    def getIRIXConfigs(self, **kwargs):
        """
        """
        args = {'portal_type':'IRIXConfig'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 

    def getTexts(self, **kwargs):
        """
        """
        args = {'portal_type':'Text'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 


##code-section bottom
##/code-section bottom 
