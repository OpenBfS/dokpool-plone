from pkg_resources import get_distribution
from Products.Five import BrowserView


class ContextHelpers(BrowserView):
    """Stuff that previously were skin scripts"""

    def is_archive(self):
        return "archive" in self.context.getPhysicalPath()


class DokpoolVersion(BrowserView):
    def __call__(self):
        dist = get_distribution("docpool.base")
        return dist.version
