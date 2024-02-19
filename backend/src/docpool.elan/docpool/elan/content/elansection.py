from docpool.elan.config import ELAN_APP
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IELANSection(model.Schema):
    """ """


@implementer(IELANSection)
class ELANSection(Container):
    """ """

    APP = ELAN_APP
