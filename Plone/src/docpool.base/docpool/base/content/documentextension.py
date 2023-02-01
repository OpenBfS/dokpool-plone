from plone.dexterity.content import Item
from plone.supermodel import model
from zope.interface import implementer


class IDocumentExtension(model.Schema):
    """ """


@implementer(IDocumentExtension)
class DocumentExtension(Item):
    """ """
