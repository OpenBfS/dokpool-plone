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
