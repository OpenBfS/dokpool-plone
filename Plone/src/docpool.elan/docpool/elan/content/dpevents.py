from docpool.elan.config import ELAN_APP
from logging import getLogger
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

    def getDPEvents(self, **kwargs):
        """ """
        args = {"portal_type": "DPEvent"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]
