# -*- coding: utf-8 -*-
#
# File: dashboardcollection.py
#
# Copyright (c) 2015 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the DashboardCollection content type. See dashboardcollection.py for more
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
from elan.esd.content.elandoccollection import ELANDocCollection, IELANDocCollection

from Products.CMFCore.utils import getToolByName

##code-section imports
##/code-section imports 

from docpool.dashboard.config import PROJECTNAME

from docpool.dashboard import DocpoolMessageFactory as _

class IDashboardCollection(form.Schema, IELANDocCollection):
    """
    """

##code-section interface
##/code-section interface


class DashboardCollection(Item, ELANDocCollection):
    """
    """
    security = ClassSecurityInfo()
    
    implements(IDashboardCollection)
    
##code-section methods
##/code-section methods 


##code-section bottom
##/code-section bottom 
