from docpool.base.content.archiving import IArchiving
from docpool.base.utils import is_in_dp_folder
from plone.app.layout.viewlets import common
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.viewlet.interfaces import IViewletManager


class ISidebarManager(IViewletManager):
    """Custom sidebar manager"""


class ISidebarAppSpecificManager(IViewletManager):
    """App-specific viewlets in sidebar"""


class SidebarViewlet(common.ViewletBase):
    index = ViewPageTemplateFile("sidebar.pt")

    def render(self):
        # XXX Paths shouldn't be hard-coded. Maybe add a property to folders or introduce a behavior.
        if is_in_dp_folder(
            self.context,
            "content/Groups",
            "content/Transfers",
            "hintergrundinfos-ns",
        ):
            return ""
        return super().render()

    def base_url(self):
        """Return dp-url or archive-url if we're in a archive."""
        if IArchiving(self.context).is_archive and getattr(self.context, "myELANArchive", None):
            return self.context.myELANArchive().absolute_url()
        return self.navigation_root_url
