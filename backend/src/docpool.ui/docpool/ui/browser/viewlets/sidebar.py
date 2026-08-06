from docpool.base.content.archiving import IArchiving
from docpool.base.utils import is_in_dp_folder
from docpool.elan.config import ELAN_APP
from docpool.ui.browser.viewlets.header import GroupsTreeMixin
from plone import api
from plone.app.layout.viewlets import common
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.viewlet.interfaces import IViewletManager


class ISidebarManager(IViewletManager):
    """Custom sidebar manager"""


class ISidebarAppSpecificManager(IViewletManager):
    """App-specific viewlets in sidebar"""


class SidebarViewlet(GroupsTreeMixin, common.ViewletBase):
    index = ViewPageTemplateFile("sidebar.pt")
    groups_nav = ViewPageTemplateFile("sidebar-groups-nav.pt")
    section_views = {
        "chronology": {"listing"},
        "entrytypes": {"entrytypes"},
        "journals": {"journals", "journalentries"},
        "overview": {"overview"},
        "tasks": {"tasks"},
    }

    def base_url(self):
        """Return dp-url or archive-url if we're in an archive."""
        if IArchiving(self.context).is_archive and getattr(self.context, "myELANArchive", None):
            return self.context.myELANArchive().absolute_url()
        return self.navigation_root_url

    def is_active(self, section):
        # TODO Improve - Should not use getURL
        view_segment = self.request.getURL().rstrip("/").rsplit("/", 1)[-1]
        if not view_segment.startswith("@@"):
            return False

        view_name = view_segment[2:]
        return view_name in self.section_views.get(section, set())

    def update(self):
        super().update()
        if is_in_dp_folder(self.context, "content/Groups", "content/Transfers"):
            self.groups_tree = self.build_groups_tree()
        else:
            self.groups_tree = []

    def render(self):
        # XXX Paths shouldn't be hard-coded. Maybe add a property to folders or introduce a behavior.
        if is_in_dp_folder(self.context, "content/Groups", "content/Transfers"):
            return self.groups_nav()
        if is_in_dp_folder(self.context, "hintergrundinfos-ns"):
            return ""
        return super().render()

    def show_journals(self):
        dp_app_state = api.content.get_view("dp_app_state", self.context, self.request)
        active_apps = dp_app_state.appsActivatedByCurrentUser()
        if ELAN_APP not in active_apps:
            return

        journals_view = api.content.get_view("journals", self.context, self.request)
        return bool(journals_view.get_journals())

    def show_tasks(self):
        dp_app_state = api.content.get_view("dp_app_state", self.context, self.request)
        active_apps = dp_app_state.appsActivatedByCurrentUser()
        if ELAN_APP in active_apps:
            return True

    def number_of_tasks(self):
        tasks_view = api.content.get_view("tasks", self.context, self.request)
        uids, _ = tasks_view.find()
        return len(uids)
