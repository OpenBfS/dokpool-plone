from AccessControl import ClassSecurityInfo
from docpool.elan import DocpoolMessageFactory as _
from logging import getLogger
from plone.dexterity.content import Item
from plone.supermodel import model
from zope import schema
from zope.interface import implementer


logger = getLogger("dpnetwork")


class IDPNetwork(model.Schema):
    """ """

    area = schema.Text(title=_("Area coordinates"), required=False)


@implementer(IDPNetwork)
class DPNetwork(Item):
    """ """

    security = ClassSecurityInfo()
