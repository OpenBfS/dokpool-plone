from Products.ZCatalog.interfaces import ICatalogBrain
from zope.component import adapter
from zope.interface import implementer
from zope.interface import Interface


class IArchiving(Interface):
    is_archive: bool


@implementer(IArchiving)
@adapter(Interface)
class Archiving:
    def __init__(self, context):
        self.context = context

    @property
    def is_archive(self):
        return "archive" in (
            self.context.getPath().split("/")
            if ICatalogBrain.providedBy(self.context)
            else self.context.getPhysicalPath()
        )
