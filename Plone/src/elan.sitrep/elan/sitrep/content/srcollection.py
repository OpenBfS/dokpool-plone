# -*- coding: utf-8 -*-
#
# File: srcollection.py
#
# Copyright (c) 2017 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the SRCollection content type. See srcollection.py for more
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
from elan.esd.content.elandoccollection import ELANDocCollection, IELANDocCollection

from Products.CMFCore.utils import getToolByName

##code-section imports
##/code-section imports 

from elan.sitrep.config import PROJECTNAME

from elan.sitrep import DocpoolMessageFactory as _

class ISRCollection(form.Schema, IELANDocCollection):
    """
    """

##code-section interface
##/code-section interface


class SRCollection(Item, ELANDocCollection):
    """
    """
    security = ClassSecurityInfo()
    
    implements(ISRCollection)
    
##code-section methods
##/code-section methods 


##code-section bottom
##/code-section bottom 
