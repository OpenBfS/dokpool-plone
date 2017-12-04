from docpool.base.content.contentbase import IContentBase
from z3c.caching.interfaces import ILastModified
from zope.component import adapter
from zope.interface import implementer


@implementer(ILastModified)
@adapter(IContentBase)
class ContentBaseLastModified(object):
    """
    """
    def __init__(self, context):
        self.context = context

    def __call__(self):
        wdate = self.context.wdate
        if wdate is None:
            modified = self.context.modified()
            if modified is None:
                return None
            return modified.asdatetime()
        return wdate.asdatetime()