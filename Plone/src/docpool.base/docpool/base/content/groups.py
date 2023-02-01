from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IGroups(model.Schema):
    """ """


@implementer(IGroups)
class Groups(Container):
    """ """
