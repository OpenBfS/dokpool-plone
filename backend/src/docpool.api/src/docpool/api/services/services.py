from docpool.base.utils import get_docpool_for_user
from docpool.base.utils import getGroupsForCurrentUser
from plone import api
from plone.restapi.interfaces import ISerializeToJson
from plone.restapi.search.handler import SearchHandler
from plone.restapi.services import Service
from Products.PlonePAS.utils import cleanId
from zope.component import queryMultiAdapter
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse

import json


@implementer(IPublishTraverse)
class GetPrimaryDocumentpool(Service):
    """
    Return the ESD the current user belongs to - or the first one he has access to if he is a global user.
    Optionally specify a userid.

    curl -i -X GET http://localhost:8080/dokpool/@get_primary_documentpool/user1
        -H "Accept: application/json" --user admin:secret

    """

    def __init__(self, context, request):
        super().__init__(context, request)
        self.params = []

    def publishTraverse(self, request, name):
        # Consume any path segments after /@<name> as parameters
        self.params.append(name)
        return self

    def reply(self):
        if self.params:
            user = api.user.get(self.params[0])
            if user is None:
                self.request.response.setStatus(404)
                return {
                    "error": {
                        "type": "Not Found",
                        "message": "No such user: %r" % self.params[0],
                    }
                }
        else:
            user = api.user.get_current()
        obj = get_docpool_for_user(user)
        serializer = queryMultiAdapter((obj, self.request), ISerializeToJson)
        return serializer(include_items=False)


@implementer(IPublishTraverse)
class GetDocumentpools(Service):
    """
    Return the ids of all dokpools the current user belongs to

    curl -i -X GET http://localhost:8080/dokpool/@get_documentpools/user1
        -H "Accept: application/json" --user admin:secret

    """

    def __init__(self, context, request):
        super().__init__(context, request)
        self.params = []

    def publishTraverse(self, request, name):
        # Consume any path segments after /@<name> as parameters
        self.params.append(name)
        return self

    def reply(self):
        if self.params:
            try:
                with api.env.adopt_user(self.params[0]):
                    brains = api.content.find(portal_type="DocumentPool", sort_on="path")
            except api.exc.UserNotFoundError:
                self.request.response.setStatus(404)
                return {
                    "error": {
                        "type": "Not Found",
                        "message": "No such user: %r" % self.params[0],
                    }
                }
        else:
            brains = api.content.find(portal_type="DocumentPool", sort_on="path")
        return [i.id for i in brains]


@implementer(IPublishTraverse)
class GetUserFolder(Service):
    """
    Return the user folder object within the ESD.
    By default the primary docpool is used.
    Optionally specify the id of a specific docpool.

    curl -i -X GET http://localhost:8080/dokpool/@get_user_folder/bund -H "Accept: application/json" --user admin:secret
    """

    def __init__(self, context, request):
        super().__init__(context, request)
        self.params = []

    def publishTraverse(self, request, name):
        # Consume any path segments after /@<name> as parameters
        self.params.append(name)
        return self

    def reply(self):
        esdpath = None
        user = api.user.get_current()
        username = cleanId(user.getUserName())
        if self.params:
            brains = api.content.find(portal_type="DocumentPool", getId=self.params[0])
            if brains and len(brains) == 1:
                esdpath = brains[0].getPath()
        else:
            esd = get_docpool_for_user(user)
            esdpath = "/".join(esd.getPhysicalPath())
        if not esdpath:
            return
        userfolder_path = f"{esdpath}/content/Members/{username}"
        obj = api.content.get(path=userfolder_path)
        if obj:
            serializer = queryMultiAdapter((obj, self.request), ISerializeToJson)
            return serializer(include_items=False)
        else:
            self.request.response.setStatus(404)
            return dict(error=dict(message=f"User {username} has no user folder in {esdpath}"))


@implementer(IPublishTraverse)
class GetGroupFolders(Service):
    """
    Return the groups folder objects within the ESD.
    By default the primary docpool is used.
    Optionally specify the id of a specific docpool.

    curl -i -X GET http://localhost:8080/dokpool/@get_group_folders/bund -H "Accept: application/json" --user admin:secret
    """

    def __init__(self, context, request):
        super().__init__(context, request)
        self.params = []

    def publishTraverse(self, request, name):
        # Consume any path segments after /@<name> as parameters
        self.params.append(name)
        return self

    def reply(self):
        esdpath = None
        if not self.params:
            esd = get_docpool_for_user()
            esdpath = "/".join(esd.getPhysicalPath())
        else:
            brains = api.content.find(portal_type="DocumentPool", getId=self.params[0])
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


class GetScenarioHistory(Service):
    def reply(self):
        return json.loads(self.context.changelog or "[]")


@implementer(IPublishTraverse)
class GetTransferFolders(Service):
    """
    Return the groups folder objects within the ESD.
    By default the primary docpool is used.
    Optionally specify the id of a specific docpool.

    curl -i -X GET http://localhost:8080/dokpool/@get_transfer_folders/bund -H "Accept: application/json" --user admin:secret
    """

    def __init__(self, context, request):
        super().__init__(context, request)
        self.params = []

    def publishTraverse(self, request, name):
        # Consume any path segments after /@<name> as parameters
        self.params.append(name)
        return self

    def reply(self):
        esdpath = None
        if not self.params:
            esd = get_docpool_for_user()
            esdpath = "/".join(esd.getPhysicalPath())
        else:
            brains = api.content.find(portal_type="DocumentPool", getId=self.params[0])
            if brains and len(brains) == 1:
                esd = brains[0].getObject()
                esdpath = brains[0].getPath()
        if not esdpath:
            return

        query = {
            "portal_type": "DPTransferFolder",
            "path": esdpath + "/content/Transfers",
        }
        return SearchHandler(self.context, self.request).search(query)
