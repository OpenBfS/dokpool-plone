from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IDocTypes(model.Schema):
    """ """


@implementer(IDocTypes)
class DocTypes(Container):
    """ """

    APP = "base"
