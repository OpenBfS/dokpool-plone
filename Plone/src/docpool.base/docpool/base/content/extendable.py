# -*- coding: utf-8 -*-
#
# File: extendable.py
#
# Copyright (c) 2016 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the Extendable content type. See extendable.py for more
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

from Products.CMFCore.utils import getToolByName

##code-section imports
from docpool.base.appregistry import APP_REGISTRY
from docpool.base.utils import getActiveAllowedPersonalBehaviorsForDocument
##/code-section imports

from docpool.base.config import PROJECTNAME

from docpool.base import DocpoolMessageFactory as _

class IExtendable(form.Schema):
    """
    """

##code-section interface
##/code-section interface


class Extendable(Item):
    """
    """
    security = ClassSecurityInfo()
    
    implements(IExtendable)
    
##code-section methods
    def doc_extension(self, applicationName):
        """
        Get the object for the extension related to the given application.
        @param applicationName: the name of the application
        @return: the extension object
        """
        return APP_REGISTRY[applicationName]['documentBehavior'](self) # and APP_REGISTRY[applicationName]['documentBehavior'](self) or self

    def type_extension(self, applicationName):
        return APP_REGISTRY[applicationName]['typeBehavior'](self) # and APP_REGISTRY[applicationName]['typeBehavior'](self) or self

    # FIXME: potential performance leak
    def myExtensions(self, request):
        """

        @return:
        """
        behaviorNames = getActiveAllowedPersonalBehaviorsForDocument(self, request)
        print "myExtensions", behaviorNames
        return [ self.doc_extension(name) for name in behaviorNames ]
##/code-section methods


##code-section bottom
##/code-section bottom 
