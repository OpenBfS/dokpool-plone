# -*- coding: utf-8 -*-
#
# File: elanarchive.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the ELANArchive content type. See elanarchive.py for more
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

from Products.CMFCore.utils import getToolByName

##code-section imports
from docpool.elan.config import ELAN_APP
from docpool.base.interfaces import IApplicationAware
from zope.interface.declarations import classImplements
##/code-section imports 

from elan.esd.config import PROJECTNAME

from elan.esd import DocpoolMessageFactory as _

class IELANArchive(form.Schema):
    """
    """

##code-section interface
##/code-section interface


class ELANArchive(Container):
    """
    """
    security = ClassSecurityInfo()
    
    implements(IELANArchive)
    
##code-section methods
    APP = ELAN_APP

    def isSituationDisplay(self):
        """
        Marker for portlets
        """
        return 1
##/code-section methods 

    def myELANArchive(self):
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

    def getContentAreas(self, **kwargs):
        """
        """
        args = {'portal_type':'ContentArea'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 

    def getELANCurrentSituations(self, **kwargs):
        """
        """
        args = {'portal_type':'ELANCurrentSituation'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 


##code-section bottom
classImplements(ELANArchive,IApplicationAware)
##/code-section bottom 
