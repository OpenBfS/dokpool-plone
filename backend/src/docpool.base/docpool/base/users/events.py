from logging import getLogger
from plone import api
from Products.PlonePAS.utils import cleanId
from Products.PluggableAuthService.interfaces.events import IPrincipalDeletedEvent
from zope.component import adapter


logger = getLogger(__name__)


@adapter(IPrincipalDeletedEvent)
def pricipaldeleted_handler(obj):
    """Delete UserFolders for a deleted user."""
    username = cleanId(obj.principal)
    for brain in api.content.find(portal_type="UserFolder", id=username):
        folder = brain.getObject()
        logger.info("Deleting UserFolder %s", folder.absolute_url())
        api.content.delete(folder, check_linkintegrity=False)
