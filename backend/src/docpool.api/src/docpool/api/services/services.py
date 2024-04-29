from docpool.base.utils import get_docpool_for_user
from docpool.base.utils import getGroupsForCurrentUser
from plone import api
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.search.handler import SearchHandler
from plone.restapi.services import Service
from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse


class GetPrimaryDocumentpool(Service):
    """
    Return the ESD the user belongs to - or the first one he has access to if he is a global user.

    curl -i -X GET http://localhost:8081/dokpool/@get_primary_documentpool
        -H "Accept: application/json" --user admin:secret
    """

    def reply(self):
        obj = get_docpool_for_user()
        serializer = queryMultiAdapter((obj, self.request), ISerializeToJson)
        return serializer(include_items=False)


@implementer(IPublishTraverse)
class GetUserFolder(Service):
    """
    Return the user folder object within the ESD.
    By default the primary docpool is used.
    Optionally specify the id of a specific docpool.

    curl -i -X GET http://localhost:8081/dokpool/@get_user_folder/bund -H "Accept: application/json" --user admin:secret
    """

    def __init__(self, context, request):
        super(GetUserFolder, self).__init__(context, request)
        self.esdname = None

    def publishTraverse(self, request, name):
        if self.esdname is None:
            self.esdname = name
        return self

    def reply(self):
        esdpath = None
        user = api.user.get_current()
        username = user.getUserName().replace("-", "--")
        if not self.esdname:
            esd = get_docpool_for_user(user)
            esdpath = "/".join(esd.getPhysicalPath())
        else:
            brains = api.content.find(portal_type="DocumentPool", getId=self.esdname)
            if brains and len(brains) == 1:
                esdpath = brains[0].getPath()
        if not esdpath:
            return
        userfolder_path = "{}/content/Members/{}".format(esdpath, username)
        obj = api.content.get(path=userfolder_path)
        if obj:
            serializer = queryMultiAdapter((obj, self.request), ISerializeToJson)
            return serializer(include_items=False)


@implementer(IPublishTraverse)
class GetGroupFolders(Service):
    """
    Return the groups folder objects within the ESD.
    By default the primary docpool is used.
    Optionally specify the id of a specific docpool.

    curl -i -X GET http://localhost:8081/dokpool/@get_group_folders/bund -H "Accept: application/json" --user admin:secret
    """

    def __init__(self, context, request):
        super(GetGroupFolders, self).__init__(context, request)
        self.esdname = None

    def publishTraverse(self, request, name):
        if self.esdname is None:
            self.esdname = name
        return self

    def reply(self):
        esdpath = None
        if not self.esdname:
            esd = get_docpool_for_user()
            esdpath = "/".join(esd.getPhysicalPath())
        else:
            brains = api.content.find(portal_type="DocumentPool", getId=self.esdname)
            if brains and len(brains) == 1:
                esd = brains[0].getObject()
                esdpath = brains[0].getPath()
        if not esdpath:
            return

        groups = getGroupsForCurrentUser(esd)
        if not groups:  # User is reader only
            return {}
        ids = []
        for group in groups:
            if group["etypes"]:  # Group is ELAN group which can produce documents
                ids.append(group["id"])

        # TODO: What data do we actually want? Maybe add metadata_fields or fullobjects?
        query = {
            "portal_type": "GroupFolder",
            "path": esdpath + "/content/Groups",
            "getId": ids,
        }
        return SearchHandler(self.context, self.request).search(query)
