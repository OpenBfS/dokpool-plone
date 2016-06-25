# -*- coding: utf-8 -*-
#
# File: srmoduletype.py
#
# Copyright (c) 2016 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the SRModuleType content type. See srmoduletype.py for more
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
from docpool.base.content.doctype import DocType, IDocType

from Products.CMFCore.utils import getToolByName

##code-section imports
##/code-section imports 

from elan.sitrep.config import PROJECTNAME

from elan.sitrep import DocpoolMessageFactory as _

class ISRModuleType(form.Schema, IDocType):
    """
    """
        
    docSelection = RelationChoice(
                        title=_(u'label_srmoduletype_docselection', default=u'Collection for relevant documents'),
                        description=_(u'description_srmoduletype_docselection', default=u'This collection defines a pre-selection of possible documents to reference within this module.'),
                        required=False,
##code-section field_docSelection
                        source = "elan.sitrep.vocabularies.Collections",
##/code-section field_docSelection                           
    )
    

##code-section interface
    form.widget(docSelection='z3c.form.browser.select.SelectFieldWidget')
    
    form.mode(allowUploads='hidden')
    form.mode(publishImmediately='hidden')
    form.mode(globalAllow='hidden')
#    form.mode(allowedDocTypes='hidden') # does not work --> done in CSS
    form.mode(partsPattern='hidden')
    form.mode(pdfPattern='hidden')
    form.mode(imgPattern='hidden')
    form.mode(customViewTemplate='hidden')
##/code-section interface


class SRModuleType(Container, DocType):
    """
    """
    security = ClassSecurityInfo()
    
    implements(ISRModuleType)
    
##code-section methods
    def currentDocuments(self):
        """
        Return the documents from the referenced collection - if any.
        """
        if self.docSelection:
            coll = self.docSelection.to_object
            return coll.results(batch=False)
        else:
            return []
##/code-section methods 

    def mySRModuleType(self):
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
