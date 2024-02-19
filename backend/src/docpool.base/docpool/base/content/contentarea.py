from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IContentArea(model.Schema):
    """ """


@implementer(IContentArea)
class ContentArea(Container):
    """ """
