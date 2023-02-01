from docpool.elan.config import ELAN_APP
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IELANArchives(model.Schema):
    """ """


@implementer(IELANArchives)
class ELANArchives(Container):
    """ """

    APP = ELAN_APP
