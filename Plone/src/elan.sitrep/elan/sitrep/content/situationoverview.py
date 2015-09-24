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
##/code-section methods 


##code-section bottom
##/code-section bottom 
