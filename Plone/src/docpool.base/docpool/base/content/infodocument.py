# -*- coding: utf-8 -*-
#
# File: infodocument.py
#
# Copyright (c) 2016 by Condat AG
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

from plone.dexterity.content import Container
from plone.app.contenttypes.content import Document,IDocument

from Products.CMFCore.utils import getToolByName

##code-section imports
##/code-section imports 

from docpool.base.config import PROJECTNAME

from docpool.base import ELAN_EMessageFactory as _

class IInfoDocument(form.Schema, IDocument):
    """
    """
    dexteritytextindexer.searchable('text')    
    text = RichText(
                        title=_(u'label_infodocument_text', default=u'Text'),
                        description=_(u'description_infodocument_text', default=u''),
                        required=True,
##code-section field_text
##/code-section field_text                           
    )
    

##code-section interface
##/code-section interface


class InfoDocument(Container, Document):
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

    def myInfoDocument(self):
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

    def getFiles(self, **kwargs):
        """
        """
        args = {'portal_type':'File'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 

    def getImages(self, **kwargs):
        """
        """
        args = {'portal_type':'Image'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)] 


##code-section bottom
##/code-section bottom 
