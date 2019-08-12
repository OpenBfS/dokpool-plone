# -*- coding: utf-8 -*-


__author__ = ''
__docformat__ = 'plaintext'

from AccessControl import ClassSecurityInfo
from docpool.event import DocpoolMessageFactory as _
from logging import getLogger
from plone.dexterity.content import Item
from plone.directives import form
from zope import schema
from zope.interface import implements


logger = getLogger("dpnetwork")


class IDPNetwork(form.Schema):
    """
    """

    area = schema.Text(title=_(u"Area coordinates"), required=False)


class DPNetwork(Item):
    """
    """

    security = ClassSecurityInfo()

    implements(IDPNetwork)
