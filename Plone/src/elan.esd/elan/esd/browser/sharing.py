from plone.app.workflow.browser.sharing import SharingView as OSV
from plone.memoize.instance import memoize


class SharingView(OSV):
    @memoize
    def roles(self):
        """
        Reduce the available roles for sharing
        """
        pairs = OSV.roles(self)
        return [p for p in pairs if p['id'] == 'Reader']
