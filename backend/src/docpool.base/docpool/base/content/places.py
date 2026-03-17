from Acquisition import aq_base
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


def container_with_portal_type(obj, portal_type):
    while obj is not None and getattr(aq_base(obj), "portal_type", None) != portal_type:
        obj = ILocation(obj).__parent__
    return obj


@adapter(Interface)
@implementer(IPlaces)
class PlacesAPI:
    def __init__(self, context):
        self.context = context

    @property
    def document_pool(self):
        return container_with_portal_type(self.context, "DocumentPool")

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
        return container_with_portal_type(self.context, "ContentArea") is not None
