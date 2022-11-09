from AccessControl import ClassSecurityInfo
from docpool.elan.config import ELAN_APP
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IELANCurrentSituation(model.Schema):
    pass


@implementer(IELANCurrentSituation)
class ELANCurrentSituation(Container):

    security = ClassSecurityInfo()

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

    def getFirstChild(self):
        fc = self.getFolderContents()
        if len(fc) > 0:
            return fc[0].getObject()
        else:
            return None

    def getAllContentObjects(self):
        return [obj.getObject() for obj in self.getFolderContents()]
