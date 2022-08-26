from AccessControl import ClassSecurityInfo
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


class IDashboardsConfig(model.Schema):
    """ """


@implementer(IDashboardsConfig)
class DashboardsConfig(Container):

    security = ClassSecurityInfo()

    def myDashboardsConfig(self):
        """ """
        return self

    def getFirstChild(self):
        """ """
        fc = self.getFolderContents()
        if len(fc) > 0:
            return fc[0].getObject()
        else:
            return None

    def getAllContentObjects(self):
        """ """
        return [obj.getObject() for obj in self.getFolderContents()]
