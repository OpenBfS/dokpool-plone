from plone.app.layout.viewlets.common import ViewletBase


class ManagePortletsFallbackViewlet(ViewletBase):
    """Manage portlets fallback link that sits below content"""

    def index(self):
        return ""

    def update(self):
        pass
