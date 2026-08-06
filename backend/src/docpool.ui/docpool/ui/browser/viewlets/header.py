from App.config import getConfiguration
from docpool.base import DocpoolMessageFactory as _
from docpool.base.appregistry import appLogo as appLogo
from docpool.base.appregistry import appName
from docpool.base.config import BASE_APP
from docpool.base.config import TRANSFERS_APP
from docpool.base.content.archiving import IArchiving
from docpool.base.content.places import IPlaces
from docpool.base.utils import is_in_dp_folder
from docpool.elan import DocpoolMessageFactory as EMF
from docpool.elan.content.elanarchive import IELANArchive
from docpool.elan.utils import get_scenario_for_current_user
from docpool.elan.utils import getOpenScenarios
from docpool.ui.browser.viewlets.footer import TimezoneTableMixin
from docpool.ui.utils import can_view
from importlib.metadata import distribution
from plone import api
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.navtree import buildFolderTree
from plone.app.layout.viewlets.common import SearchBoxViewlet
from plone.app.layout.viewlets.common import ViewletBase
from plone.base.i18nl10n import utranslate
from Products.CMFPlone.browser.navtree import DefaultNavtreeStrategy
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
from zope.viewlet.interfaces import IViewletManager

import os
import shlex
import subprocess


class IHeaderNavManager(IViewletManager):
    """Custom header navigation manager"""


class EventSwitcherMixin:
    def set_scenario_attributes(self):
        possible = [s for s in getOpenScenarios(self.context) if s.review_state == "published"]
        scenarios_by_uid = {s.UID: s.getObject() for s in possible}
        selected_uid = get_scenario_for_current_user(self.context)
        self.selected_scenario = scenarios_by_uid.get(selected_uid)
        return scenarios_by_uid, selected_uid


class GroupsTreeMixin:
    def build_groups_tree(self):
        content_area = IPlaces(self.context).content
        if content_area is None:
            return []

        result = []
        for folder_id, item_class in (("Groups", None), ("Transfers", "transfer")):
            folder = content_area.get(folder_id)
            if folder is None:
                continue

            folder_path = "/".join(folder.getPhysicalPath())
            query = {
                "path": {"query": folder_path, "depth": 999, "navtree": 1, "navtree_start": 1},
                "portal_type": ["DPTransferFolder", "GroupFolder", "SimpleFolder"],
                "sort_on": ["portal_type", "sortable_title"],
                "apps_supported": self.active_apps_for_tree(),
            }

            strategy = getMultiAdapter((self.context, None), INavtreeStrategy)
            if strategy is None:
                strategy = DefaultNavtreeStrategy(self.context)
            strategy.rootPath = folder_path
            strategy.bottomLevel = 999

            tree = buildFolderTree(self.context, obj=self.context, query=query, strategy=strategy)
            children = tree.get("children", [])
            if item_class:
                for node in children:
                    node["item_class"] = item_class
            result.extend(children)

        return result

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


class AppSearchBoxViewlet(SearchBoxViewlet):
    search_placeholders = {
        "rodos": _("Search RODOS"),
        "doksys": _("Search DokSys"),
        "rei": _("Search REI"),
    }

    def update(self):
        super().update()
        dp_app_state = api.content.get_view("dp_app_state", self.context, self.request)
        active_apps = dp_app_state.appsActivatedByCurrentUser()
        current_app = active_apps[0] if active_apps else None
        placeholder = self.search_placeholders.get(
            current_app,
            _("Search ELAN"),
        )
        self.search_placeholder = utranslate("docpool.base", placeholder, context=self.request)


class PortalHeader(EventSwitcherMixin, TimezoneTableMixin, GroupsTreeMixin, ViewletBase):
    redirect_to_map = {
        "base": "",
        "elan": "/@@overview",
        "doksys": "/@@listing",
        "rei": "/@@listing",
        "rodos": "/@@listing",
    }

    def update(self):
        super().update()
        self.dp, self.app, self.dp_apps = getApplicationDocPoolsForCurrentUser(self.context, self.request)
        self.dp_url = self.dp.absolute_url() if self.dp else None
        self.app_logo = appLogo(self.app) if self.app else None
        self.set_scenario_attributes()

        # Prepare mobile folder tree navigation
        if is_in_dp_folder(self.context, "content/Groups", "content/Transfers"):
            self.groups_tree = self.build_groups_tree()
        else:
            self.groups_tree = []

        try:
            self.groups_folder_url = self.dp["content"]["Groups"].absolute_url()
        except BaseException:
            self.groups_folder_url = None
        try:
            self.emergency_info_url = self.dp["hintergrundinfos-ns"].absolute_url()
        except BaseException:
            self.emergency_info_url = None

        url = self.request.getURL()
        self.active = {
            key: (
                "nav-active"
                if any(
                    (url == (vurl := f"{self.dp_url}{val}")) or url.startswith(f"{vurl}/") for val in value
                )
                else ""
            )
            for key, value in dict(
                groups=["/content/Groups", "/content/Transfers"],
                emergency=["/hintergrundinfos-ns"],
            ).items()
        }

    def apps_menu(self):
        current_dp_id = self.dp.getId() if self.dp else None
        all_apps = sorted(
            (appName(name), name) for name in set().union(*[names for _, names in self.dp_apps])
        )
        menu = []

        for dp, _app_names in self.dp_apps:
            dp_id = dp.getId()
            physical_path = self.context.getPhysicalPath()
            keep_context = (
                current_dp_id == dp_id and "content" in physical_path and "archive" not in physical_path
            )
            url = (self.context if keep_context else dp).absolute_url()
            apps = []
            for app_title, app_name in all_apps:
                redirect_to = self.redirect_to_map.get(app_name)
                params = "" if keep_context or redirect_to is None else f"&redirect_to={redirect_to}"
                apps.append(
                    dict(
                        title=f"{app_title}",
                        url=f"{url}/setActiveApp?app={app_name}{params}",
                    )
                )

            menu.append(
                dict(
                    dptitle=dp.title,
                    selected=dp_id == current_dp_id,
                    apps=apps,
                )
            )

        return menu


class EventSwitcherViewlet(EventSwitcherMixin, ViewletBase):
    def update(self):
        super().update()
        self.dp = IPlaces(self.context).document_pool
        if self.dp is None:
            return

        self.dp_url = self.dp.absolute_url()
        self.set_scenario_attributes()

        self.is_archive = False
        if IArchiving(self.context).is_archive:
            self.is_archive = True
            if self.context.portal_type in ["ELANArchives", "ELANArchive"]:
                self.selected_scenario = self.context
            else:
                self.selected_scenario = api.content.get_closest_ancestor(
                    self.context, interface=IELANArchive
                )

        url = self.request.getURL()
        self.active = (
            "nav-active"
            if any(
                (url == (vurl := f"{self.dp_url}{val}")) or url.startswith(f"{vurl}/")
                for val in [
                    "/esd",
                    "/",
                    "/config/dtypes",
                ]
            )
            else ""
        )


class EventSwitcherDropdown(EventSwitcherMixin, BrowserView):
    def __call__(self):

        self.dp = IPlaces(self.context).document_pool
        if self.dp is None:
            return

        self.dp_url = self.dp.absolute_url()

        scenarios_by_uid, selected_uid = self.set_scenario_attributes()
        self.scenarios = []
        status_vocabulary = api.portal.get_vocabulary(
            "docpool.elan.vocabularies.Status", context=self.context
        )
        for status_term in status_vocabulary:
            scenarios = [
                dict(
                    scenario=s,
                    selected=(uid == selected_uid),
                    last=False,
                    actions=self._actions(s),
                )
                for uid, s in scenarios_by_uid.items()
                if s.Status == status_term.value
            ]
            if scenarios:
                scenarios[-1]["last"] = True
                self.scenarios.extend(scenarios)
        return super().__call__()

    def _actions(self, event):
        event_url = event.absolute_url()
        actions = []
        if can_view(event, "@@edit"):
            actions.append(dict(url=f"{event_url}/@@edit", icon="pencil", text="Edit"))
        if can_view(self.dp, "@@archiveAndClose"):
            actions.append(
                dict(
                    url=f"{self.dp_url}/@@archiveAndClose?event={event.UID()}",
                    icon="archive-fill",
                    text=EMF("Archiving"),
                )
            )
        if can_view(self.dp, "@@snapshot"):
            actions.append(
                dict(
                    url=f"{self.dp_url}/@@snaphot?event={event.UID()}",
                    icon="archive-fill",
                    text=EMF("Snapshot"),
                )
            )
        return actions


class SearchContextView(EventSwitcherMixin, BrowserView):
    def __call__(self):
        self.dp = IPlaces(self.context).document_pool
        self.dp_url = self.dp.absolute_url() if self.dp is not None else None
        scenarios_by_uid, selected_uid = self.set_scenario_attributes()
        self.selected_uid = selected_uid
        self.active_scenarios = [
            scenario
            for _, scenario in scenarios_by_uid.items()
            if getattr(scenario, "Status", None) == "active"
        ][:2]
        return self


class InfoDropdown(BrowserView):
    def get_dokpool_version(self):
        dist = distribution("docpool.base")
        return dist.version

    def available(self):
        if api.user.is_anonymous():
            return False
        if api.portal.get_registry_record(name="docpool.show_debug_info"):
            return True

    def read_git_version_file(self, filename):
        read_file = False
        file_path = ""
        # Try to get the path from the pid file :)
        try:
            varbase = os.path.dirname(getConfiguration().pid_filename)
            project_root = os.path.abspath(os.path.join(varbase, ".."))
            file_path = os.path.join(project_root, filename)
        except AttributeError:
            # Ignore if we have no access to file
            pass

        if os.path.isfile(file_path):
            read_file = True

        # New Plone backend docker structure
        if os.path.isfile("/app/GIT_COMMIT"):
            file_path = os.path.join("/app/GIT_COMMIT")
            read_file = True

        if not read_file:
            return

        with open(file_path) as file:
            content = file.read().strip()
            if content:
                return content

    def get_git_rev(self):
        # Git Revision

        # If run inside docker with existing version file
        version_in_file = self.read_git_version_file("GIT_COMMIT")
        if version_in_file:
            return version_in_file

        # If run on the review server
        commit_hash = os.getenv("GIT_COMMIT")
        if commit_hash:
            return commit_hash

        # If run local
        result = subprocess.run(
            shlex.split("git rev-parse --short HEAD"),
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 128:
            return "Not detected"

        return result.stdout.strip()

    def get_git_branch(self):
        # Git Branch
        commit_name = os.getenv("GIT_REF_NAME")
        if commit_name:
            return commit_name

        result = subprocess.run(
            shlex.split("git rev-parse --abbrev-ref HEAD"),
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode == 128:
            return "Not detected"

        return result.stdout.strip()


class UserDropdown(BrowserView):
    def user_name(self):
        if not api.user.is_anonymous():
            user = api.user.get_current()
            fullname = user.getProperty("fullname")
            return fullname or user.getId()


class ConfigDropdown(BrowserView):
    @property
    def events_url(self):
        if (dp := IPlaces(self.context).document_pool) is not None:
            return f"{dp.absolute_url()}/contentconfig/scen"
        else:
            return f"{api.portal.get().absolute_url()}/contentconfig/events"


class SystemMessagesDropdown(BrowserView):
    pass


class AccessibilityDropdown(BrowserView):
    pass


def getApplicationDocPoolsForCurrentUser(context, request):
    """
    Determine all DocPools and their applications that the user has access to.
    """
    dp_app_state = api.content.get_view("dp_app_state", context, request)
    active_apps = dp_app_state.appsActivatedByCurrentUser()
    current_app = active_apps[0] if active_apps else None
    current_dp = IPlaces(context).document_pool

    dps = (dp.getObject() for dp in api.content.find(portal_type="DocumentPool"))
    ordering = api.portal.get().getOrdering()

    # Quick and dirty safeguard against DocumentPools not living directly in the portal.
    # Shouldn't happen but DocumentPool is globally allowed so just make sure.
    def sort_key(dp):
        try:
            return ordering.getObjectPosition(dp.getId())
        except ValueError:
            return 0

    pools = []
    for dp in sorted(dps, key=sort_key):
        dp_app_state = api.content.get_view("dp_app_state", dp, request)
        app_names = dp_app_state.appsAvailableToCurrentUser()

        if app_names:
            pools.append((dp, app_names))

    return current_dp, current_app, pools
