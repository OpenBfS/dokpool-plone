from docpool.elan.config import ELAN_APP
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
        from docpool.base.utils import queryForObjects

        ecs = queryForObjects(self, path=mpath, portal_type="ELANDocCollection")
        for ec in ecs:
            ec.getObject().correctDocTypes()

    def myELANCurrentSituation(self):
        return self
