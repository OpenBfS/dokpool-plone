from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IDocTypeCategory(model.Schema):
    """ """


@implementer(IDocTypeCategory)
class DocTypeCategory(Container):
    """ """

    APP = "base"
