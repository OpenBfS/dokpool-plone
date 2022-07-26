#
# File: infodocument.py
#
# Copyright (c) 2016 by Bundesamt für Strahlenschutz
# Generator: ConPD2
#            http://www.condat.de
#

__author__ = ""
__docformat__ = "plaintext"

"""Definition of the InfoDocument content type. See infodocument.py for more
explanation on the statements below.
"""
from AccessControl import ClassSecurityInfo
from docpool.base.content.dpdocument import DPDocument, IDPDocument
from plone.autoform import directives
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class IInfoDocument(model.Schema, IDPDocument):
    """ """

    directives.mode(docType="hidden")
    docType = schema.Choice(
        required=True,
        source="docpool.base.vocabularies.DocumentTypes",
        default="infodoc",
    )


@implementer(IInfoDocument)
class InfoDocument(DPDocument):
    """ """

    security = ClassSecurityInfo()

    def dp_type(self):
        return "General"

    def category(self):
        return []

    def dp_type_name(self):
        return "General"

    def typeAndCat(self):
        """ """
        return (None, [])

    def uploadsAllowed(self):
        return True

    def getScenarios(self):
        return []

    def myInfoDocument(self):
        """ """
        return self

    def getFirstChild(self):
        """ """
        fc = self.getFolderContents()
        if len(fc) > 0:
            return fc[0].getObject()
        else:
            return None

    def getAllContentObjects(self):
        """ """
        return [obj.getObject() for obj in self.getFolderContents()]

    def getDPDocuments(self, **kwargs):
        """ """
        args = {"portal_type": "DPDocument"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getFiles(self, **kwargs):
        """ """
        args = {"portal_type": "File"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def getImages(self, **kwargs):
        """ """
        args = {"portal_type": "Image"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]
