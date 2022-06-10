from Products.Five import BrowserView
from pkg_resources import get_distribution


class ContextHelpers(BrowserView):
    """Stuff that previously were skin scripts"""

    def is_archive(self):
        return "archive" in self.context.getPhysicalPath()

    def dokpool_version(self):
        dist = get_distribution("docpool.base")
        return dist.version