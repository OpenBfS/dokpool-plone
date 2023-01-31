from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IUsers(model.Schema):
    """ """


@implementer(IUsers)
class Users(Container):
    """ """
