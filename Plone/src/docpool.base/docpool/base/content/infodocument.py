# -*- coding: utf-8 -*-
#
# File: infodocument.py
#
# Copyright (c) 2015 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the InfoDocument content type. See infodocument.py for more
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
from plone.app.contenttypes.content import Document,IDocument

from Products.CMFCore.utils import getToolByName

##code-section imports
##/code-section imports 

from docpool.base.config import PROJECTNAME

from docpool.base import ELAN_EMessageFactory as _

class IInfoDocument(form.Schema, IDocument):
    """
    """

##code-section interface
##/code-section interface


class InfoDocument(Item, Document):
    """
    """
    security = ClassSecurityInfo()
    
    implements(IInfoDocument)
    
##code-section methods
    def dp_type(self):
        return "General"


    def category(self):
        return []


    def dp_type_name(self):
        return "General"

    def typeAndCat(self):
        """
        """
        return (None, [])
    
    def uploadsAllowed(self):
        return True

    def getScenarios(self):
        return []
##/code-section methods 


##code-section bottom
##/code-section bottom 
