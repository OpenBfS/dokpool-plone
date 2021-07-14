from plone.dexterity.content import Item
from plone.supermodel import model
from zope.interface import implementer


class IIRIXConfig(model.Schema):
    pass


@implementer(IIRIXConfig)
class IRIXConfig(Item):
    """
    """
