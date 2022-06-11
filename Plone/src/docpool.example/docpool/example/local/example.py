from docpool.base.content.documentpool import APPLICATIONS_KEY
from docpool.example.config import EXAMPLE_APP
from Products.CMFCore.utils import getToolByName
from zope.annotation.interfaces import IAnnotations


def dpAdded(self):
    """
    @param self:
    @return:

    """
    annotations = IAnnotations(self)
    fresh = EXAMPLE_APP not in annotations[APPLICATIONS_KEY]
    if fresh:
        annotations[APPLICATIONS_KEY].append(EXAMPLE_APP)

    if fresh:
        createExampleGroups(self)
        # TODO:


def dpRemoved(self):
    """
    @param self:
    @return:
    """
    # TODO:
    return


def createExampleGroups(self):
    """
    Create Group for example application access
    @param self:
    @return:
    """

    prefix = self.prefix or self.getId()
    prefix = str(prefix)
    title = self.Title()
    gtool = getToolByName(self, "portal_groups")
    # Group for Example application rights
    props = {
        "allowedDocTypes": [],
        "title": "Example Users (%s)" % title,
        "description": "Users with access to Example functions.",
        "dp": self.UID(),
    }
    gtool.addGroup("%s_ExampleUsers" % prefix, properties=props)
    gtool.addPrincipalToGroup("%s_dpadmin" % prefix, "%s_ExampleUsers" % prefix)

    # Set Example role as a local role for the new group
    self.manage_setLocalRoles("%s_ExampleUsers" % prefix, ["ExampleUser"])
