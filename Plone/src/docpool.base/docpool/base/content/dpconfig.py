# -*- coding: utf-8 -*-
#
# File: dpconfig.py
#
# Copyright (c) 2015 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the DPConfig content type. See dpconfig.py for more
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

from docpool.base.config import PROJECTNAME

from docpool.base import ELAN_EMessageFactory as _

class IDPConfig(form.Schema):
    """
    """

##code-section interface
##/code-section interface


class DPConfig(Container):
    """
    """
    security = ClassSecurityInfo()
    
    implements(IDPConfig)
    
##code-section methods
##/code-section methods 

    def myDPConfig(self):
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

    def getDocTypess(self, **kwargs):
        """
        """
        args = {'portal_type':'DocTypes'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 


##code-section bottom
##/code-section bottom 
