from docpool.elan import DocpoolMessageFactory as _
from docpool.elan.config import ELAN_APP
from plone.dexterity.content import Item
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


class IDPNuclearPowerStation(model.Schema):
    """ """

    coordinates = schema.TextLine(title=_("Coordinates"), required=False)


@implementer(IDPNuclearPowerStation)
class DPNuclearPowerStation(Item):
    """ """

    APP = ELAN_APP
