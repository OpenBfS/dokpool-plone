from docpool.elan.config import ELAN_APP
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IELANArchive(model.Schema):
    """ """


@implementer(IELANArchive)
class ELANArchive(Container):
    """ """

    APP = ELAN_APP

    def myELANArchive(self):
        """ """
        return self
