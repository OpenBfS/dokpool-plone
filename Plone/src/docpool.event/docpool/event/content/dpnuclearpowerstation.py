# -*- coding: utf-8 -*-


__author__ = ''
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from zope.interface import implements
from zope import schema
from plone.directives import form, dexterity

from plone.dexterity.content import Item
from logging import getLogger
logger = getLogger("dpnetwork")

from docpool.event import DocpoolMessageFactory as _

class IDPNuclearPowerStation(form.Schema):
    """
    """
    coordinates = schema.TextLine(
        title=_(u'Coordinates'),
        required=False)

class DPNuclearPowerStation(Item):
    """
    """
    security = ClassSecurityInfo()
    
    implements(IDPNuclearPowerStation)
    
