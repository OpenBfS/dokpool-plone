from Acquisition import aq_base
from Acquisition import aq_get
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
    content_type = "ContentArea"

    @property
    def content(self):
        # XXX temporarily copied logic from old get_content_area
        if self.context.portal_type == self.content_type:
            return self.context

        if content_area := aq_get(self.context, self.content_id, None):
            if content_area.portal_type == self.content_type:
                return content_area

    @property
    def content_path(self):
        return "/".join(ca.getPhysicalPath()) if (ca := self.content) is not None else None

    @property
    def in_content(self):
        # XXX also look at id?
        return container_with_portal_type(self.context, self.content_type) is not None
