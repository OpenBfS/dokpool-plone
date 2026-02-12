from docpool.elan.config import ELAN_APP
from plone import api
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IELANCurrentSituation(model.Schema):
    pass


@implementer(IELANCurrentSituation)
class ELANCurrentSituation(Container):
    APP = ELAN_APP

    def correctAllDocTypes(self):
        # Correct references
        mpath = self.dpSearchPath()

        ecs = api.content.find(path=mpath, portal_type="ELANDocCollection")
        for ec in ecs:
            ec.getObject().correctDocTypes()

    def myELANCurrentSituation(self):
        return self
