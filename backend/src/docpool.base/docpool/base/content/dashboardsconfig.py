from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IDashboardsConfig(model.Schema):
    """ """


@implementer(IDashboardsConfig)
class DashboardsConfig(Container):
    """ """

    APP = "base"
