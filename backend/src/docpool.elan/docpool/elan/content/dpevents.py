from docpool.elan.config import ELAN_APP
from logging import getLogger
from plone import api
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


logger = getLogger("dpevents")


class IDPEvents(model.Schema):
    """ """


@implementer(IDPEvents)
class DPEvents(Container):
    """ """

    APP = ELAN_APP

    def getDPEvents(self):
        """ """
        query = {
            "portal_type": "DPEvent",
            "sort_on": "modified",
            "sort_order": "reverse",
        }
        return [obj.getObject() for obj in api.content.find(context=self, **query)]
