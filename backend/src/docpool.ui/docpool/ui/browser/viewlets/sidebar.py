from docpool.base.config import BASE_APP
from docpool.base.config import TRANSFERS_APP
from docpool.base.content.archiving import IArchiving
from docpool.base.content.places import IPlaces
from docpool.base.utils import is_in_dp_folder
from docpool.elan.config import ELAN_APP
from plone import api
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.navtree import buildFolderTree
from plone.app.layout.viewlets import common
from Products.CMFPlone.browser.navtree import DefaultNavtreeStrategy
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter
from zope.viewlet.interfaces import IViewletManager


class ISidebarManager(IViewletManager):
    """Custom sidebar manager"""


class ISidebarAppSpecificManager(IViewletManager):
    """App-specific viewlets in sidebar"""


class SidebarViewlet(common.ViewletBase):
    index = ViewPageTemplateFile("sidebar.pt")
    groups_nav = ViewPageTemplateFile("sidebar-groups-nav.pt")

    def update(self):
        super().update()
        if is_in_dp_folder(self.context, "content/Groups"):
            self.groups_tree = self.build_groups_tree()
        else:
            self.groups_tree = []

    def render(self):
        # XXX Paths shouldn't be hard-coded. Maybe add a property to folders or introduce a behavior.
        if is_in_dp_folder(self.context, "content/Groups"):
            return self.groups_nav()
        if is_in_dp_folder(
            self.context,
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

    def build_groups_tree(self):
        groups_folder = self.groups_folder()
        if groups_folder is None:
            return []

        groups_path = "/".join(groups_folder.getPhysicalPath())
        query = {
            "path": {"query": groups_path, "depth": 999, "navtree": 1, "navtree_start": 1},
            "portal_type": ["DPTransferFolder", "GroupFolder", "SimpleFolder"],
            "sort_on": ["portal_type", "sortable_title"],
            "apps_supported": self.active_apps_for_tree(),
        }

        strategy = getMultiAdapter((self.context, None), INavtreeStrategy)
        if strategy is None:
            strategy = DefaultNavtreeStrategy(self.context)
        strategy.rootPath = groups_path
        strategy.bottomLevel = 999

        tree = buildFolderTree(self.context, obj=self.context, query=query, strategy=strategy)
        return tree.get("children", [])

    def groups_folder(self):
        content_area = IPlaces(self.context).content
        if content_area is None:
            return None
        return content_area.get("Groups")

    # TODO Code duplication see listing.py
    def active_apps_for_tree(self):
        dp_app_state = api.content.get_view("dp_app_state", self.context, self.request)
        active_apps = list(dp_app_state.appsActivatedByCurrentUser())
        active_apps.extend([BASE_APP, TRANSFERS_APP])
        return active_apps

    def groups_tree_node_class(self, node):
        # Mod for pat-expandable
        if node.get("children"):
            if node.get("currentItem") or node.get("currentParent"):
                return "folder open"
            return "folder closed"
        return "document"

    def groups_tree_link_class(self, node):
        # Mod for pat-expandable
        classes = []
        if node.get("currentItem"):
            classes.append("current")
        if node.get("currentParent"):
            classes.append("in-path")
        return " ".join(classes) or None

    def show_journals(self):
        dp_app_state = api.content.get_view("dp_app_state", self.context, self.request)
        active_apps = dp_app_state.appsActivatedByCurrentUser()
        if ELAN_APP not in active_apps:
            return

        journals_view = api.content.get_view("journals", self.context, self.request)
        return bool(journals_view.get_journals())
