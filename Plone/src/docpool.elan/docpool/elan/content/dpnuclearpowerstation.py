from AccessControl import ClassSecurityInfo
from docpool.elan import DocpoolMessageFactory as _
from logging import getLogger
from plone.dexterity.content import Item
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


logger = getLogger("dpnetwork")


class IDPNuclearPowerStation(model.Schema):
    """ """

    coordinates = schema.TextLine(title=_("Coordinates"), required=False)


@implementer(IDPNuclearPowerStation)
class DPNuclearPowerStation(Item):
    """ """

    security = ClassSecurityInfo()
