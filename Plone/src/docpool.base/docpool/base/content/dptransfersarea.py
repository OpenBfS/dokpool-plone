from AccessControl import ClassSecurityInfo
from logging import getLogger
from plone.dexterity.content import Container
from plone.supermodel import model
from zope.interface import implementer


logger = getLogger(__name__)


class IDPTransfersArea(model.Schema):
    """ """


@implementer(IDPTransfersArea)
class DPTransfersArea(Container):
    """ """

    security = ClassSecurityInfo()

    def myDPTransfersArea(self):
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

    def getDPTransferFolders(self, **kwargs):
        """ """
        args = {"portal_type": "DPTransferFolder"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]
