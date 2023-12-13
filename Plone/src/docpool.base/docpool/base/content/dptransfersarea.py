from docpool.base.config import TRANSFERS_APP
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IDPTransfersArea(model.Schema):
    """ """


@implementer(IDPTransfersArea)
class DPTransfersArea(Container):
    """ """

    APP = TRANSFERS_APP
