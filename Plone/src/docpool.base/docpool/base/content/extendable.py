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
from docpool.base.appregistry import createTypeObject, createDocumentObject
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
    def extension(self, applicationName, create=False):
        """
        Get the subobject for the extension related to the given application.
        @param applicationName: the name of the application
        @return: the extension subobject
        """
        from docpool.base.content.doctype import IDocType
        from docpool.base.content.dpdocument import IDPDocument
        try:
            return self._getOb(applicationName)
        except:
            if create:
                if IDocType.providedBy(self):
                    return createTypeObject(applicationName, self)
                elif IDPDocument.providedBy(self):
                    return createDocumentObject(applicationName, self)
            return None

    def contextObject(self):
        return self
##/code-section methods 


##code-section bottom
##/code-section bottom 
