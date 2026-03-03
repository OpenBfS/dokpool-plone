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
        values=["infodoc"],
        default="infodoc",
    )


@implementer(IInfoDocument)
class InfoDocument(DPDocument):
    """ """

    def dp_type(self):
        return "General"

    def docTypeObj(self):
        return None

    def typeAndCat(self):
        """ """
        return (None, [])

    def uploadsAllowed(self):
        return True

    def category(self):
        return None

    def subcategory(self):
        return None
