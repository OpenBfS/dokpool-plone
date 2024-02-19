from plone.dexterity.content import Item
from plone.supermodel import model
from zope.interface import implementer


class IDocTypeExtension(model.Schema):
    """ """


@implementer(IDocTypeExtension)
class DocTypeExtension(Item):
    """ """
