from zope.component import adapter
from zope.interface import Attribute
from zope.interface import implementer
from zope.interface import Interface
from zope.location.interfaces import ILocation


class IPlaces(Interface):
    """
    API for accessing well-known places in the content hierarchy w.r.t. the context object.

    The context may be None.
    """

    document_pool_path = Attribute("Absolute path to document pool")
    document_pool = Attribute("Document pool")

    content_id = Attribute("Id of content area")
    content_path = Attribute("Relative path to content area")
    content = Attribute("Content area")
    in_content = Attribute("Is context inside a content area?")


@adapter(Interface)
@implementer(IPlaces)
class PlacesAPI:
    def __init__(self, context):
        self.context = context

    @property
    def document_pool(self):
        obj = self.context
        while obj is not None and obj.portal_type != "DocumentPool":
            obj = ILocation(obj).__parent__
        return obj

    @property
    def document_pool_path(self):
        return "/".join(dp.getPhysicalPath()) if (dp := self.document_pool) is not None else None

    content_id = "content"

    @property
    def content_path(self):
        return "/".join((dpp, self.content_id)) if (dpp := self.document_pool_path) is not None else None

    @property
    def content(self):
        return dp[self.content_id] if (dp := self.document_pool) is not None else None

    @property
    def in_content(self):
        obj = self.context
        while obj is not None and obj.portal_type != "ContentArea":
            obj = ILocation(obj).__parent__
        return obj is not None
