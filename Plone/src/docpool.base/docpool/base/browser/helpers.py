from pkg_resources import get_distribution
from Products.Five import BrowserView


class DokpoolVersion(BrowserView):
    def __call__(self):
        dist = get_distribution("docpool.base")
        return dist.version
