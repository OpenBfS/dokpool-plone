from docpool.base.content.simplefolder import ISimpleFolder
from docpool.base.content.simplefolder import SimpleFolder
from plone.app.content.browser import constraintypes
from plone.supermodel import model
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import ISelectableConstrainTypes
from zope.interface import implementer


class IGroupFolder(model.Schema, ISimpleFolder):
    """ """


@implementer(IGroupFolder)
class GroupFolder(SimpleFolder):
    """ """

    def getGroupOfFolder(self):
        """ """
        gtool = getToolByName(self, "portal_groups")
        grp = gtool.getGroupById(self.getId())
        return grp

    def myGroupFolder(self):
        """ """
        return self

    def getDPDocuments(self, **kwargs):
        """ """
        args = {"portal_type": "DPDocument"}
        args.update(kwargs)
        return [obj.getObject() for obj in self.getFolderContents(args)]

    def update_immediately_addable_types(self):
        constrain = ISelectableConstrainTypes(self)
        constrain.setConstrainTypesMode(constraintypes.ENABLED)
        constrain.setLocallyAllowedTypes(
            (
                "DPDocument",
                "SimpleFolder",
                "PrivateFolder",
                "ReviewFolder",
                "CollaborationFolder",
                "InfoFolder",
                "Collection",
            )
        )
        # retain order of allowed types just like the stock form does
        constrain.setImmediatelyAddableTypes(("DPDocument", "SimpleFolder"))
