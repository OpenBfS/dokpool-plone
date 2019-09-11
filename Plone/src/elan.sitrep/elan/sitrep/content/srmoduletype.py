# -*- coding: utf-8 -*-
#
# File: srmoduletype.py
#
# Copyright (c) 2017 by Condat AG
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ''
__docformat__ = 'plaintext'

"""Definition of the SRModuleType content type. See srmoduletype.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from docpool.base.content.doctype import DocType
from docpool.base.content.doctype import IDocType
from elan.sitrep import DocpoolMessageFactory as _
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.supermodel import model
from z3c.relationfield.schema import RelationChoice
from zope.interface import implementer


class ISRModuleType(model.Schema, IDocType):
    """
    """

    docSelection = RelationChoice(
        title=_(
            u'label_srmoduletype_docselection',
            default=u'Collection for relevant documents',
        ),
        description=_(
            u'description_srmoduletype_docselection',
            default=u'This collection defines a pre-selection of possible documents to reference within this module.',
        ),
        required=False,
        source="elan.sitrep.vocabularies.Collections",
    )

    directives.widget(docSelection='z3c.form.browser.select.SelectFieldWidget')

    directives.mode(allowUploads='hidden')
    directives.mode(publishImmediately='hidden')
    directives.mode(globalAllow='hidden')
    #    form.mode(allowedDocTypes='hidden') # does not work --> done in CSS
    directives.mode(partsPattern='hidden')
    directives.mode(pdfPattern='hidden')
    directives.mode(imgPattern='hidden')
    directives.mode(customViewTemplate='hidden')


@implementer(ISRModuleType)
class SRModuleType(Container, DocType):
    """
    """

    security = ClassSecurityInfo()

    def currentDocuments(self):
        """
        Return the documents from the referenced collection - if any.
        """
        if self.docSelection:
            coll = self.docSelection.to_object
            return coll.results(batch=False)
        else:
            return []

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
        args = {'portal_type': 'File'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getImages(self, **kwargs):
        """
        """
        args = {'portal_type': 'Image'}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]
