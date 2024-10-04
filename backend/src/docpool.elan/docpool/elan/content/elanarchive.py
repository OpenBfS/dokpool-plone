from docpool.elan.config import ELAN_APP
from plone import api
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

    def get_archived_event(self):
        """Get the DPEvent of this archive."""
        brains = api.content.find(
            context=self,
            portal_type="DPEvent",
        )
        if brains and len(brains) == 1:
            return brains[0].getObject()
