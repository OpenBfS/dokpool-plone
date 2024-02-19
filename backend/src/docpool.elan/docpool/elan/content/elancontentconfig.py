from docpool.elan.config import ELAN_APP
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IELANContentConfig(model.Schema):
    """ """


@implementer(IELANContentConfig)
class ELANContentConfig(Container):
    """ """

    APP = ELAN_APP
