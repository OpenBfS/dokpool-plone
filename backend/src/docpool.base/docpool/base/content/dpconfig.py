from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IDPConfig(model.Schema):
    """ """


@implementer(IDPConfig)
class DPConfig(Container):
    """ """

    APP = "base"
