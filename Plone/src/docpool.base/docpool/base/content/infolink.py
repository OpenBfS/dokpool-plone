# -*- coding: utf-8 -*-
#
# File: infolink.py
#
# Copyright (c) 2015 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the InfoLink content type. See infolink.py for more
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
from plone.app.contenttypes.content import Link,ILink

from Products.CMFCore.utils import getToolByName

##code-section imports
##/code-section imports 

from docpool.base.config import PROJECTNAME

from docpool.base import ELAN_EMessageFactory as _

class IInfoLink(form.Schema, ILink):
    """
    """

##code-section interface
##/code-section interface


class InfoLink(Item, Link):
    """
    """
    security = ClassSecurityInfo()
    
    implements(IInfoLink)
    
##code-section methods
##/code-section methods 


##code-section bottom
##/code-section bottom 
