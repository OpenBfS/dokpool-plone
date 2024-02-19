from docpool.base.content.dpdocument import DPDocument
from docpool.base.content.dpdocument import IDPDocument
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

    def dp_type(self):
        return "General"

    def category(self):
        return []

    def typeAndCat(self):
        """ """
        return (None, [])

    def uploadsAllowed(self):
        return True

    def getScenarios(self):
        return []
