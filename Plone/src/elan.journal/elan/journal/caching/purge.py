from elan.journal.interfaces import IJournal
from plone.app.caching.purge import ContentPurgePaths
from z3c.caching.interfaces import IPurgePaths
from zope.component import adapter
from zope.interface import implementer


@implementer(IPurgePaths)
@adapter(IJournal)
class LiveBlogPurgePaths(ContentPurgePaths):

    """Paths to purge for LiveBlog."""

    def getRelativePaths(self):
        paths = super().getRelativePaths()
        # Also adds recent-updates view to the list of urls to be purged
        url = self.context.absolute_url()
        paths.append(f'{url}/recent-updates')
        return paths
