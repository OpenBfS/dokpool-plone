# -*- coding: utf-8 -*-


__author__ = ''
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from docpool.event import DocpoolMessageFactory as _
from logging import getLogger
from plone.dexterity.content import Item
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


logger = getLogger("dpnetwork")


class IDPNuclearPowerStation(model.Schema):
    """
    """

    coordinates = schema.TextLine(title=_(u'Coordinates'), required=False)


@implementer(IDPNuclearPowerStation)
class DPNuclearPowerStation(Item):
    """
    """

    security = ClassSecurityInfo()
