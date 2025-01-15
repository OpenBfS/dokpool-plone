from Acquisition import aq_get
from docpool.base.appregistry import appName
from docpool.base.config import BASE_APP
from docpool.base.config import TRANSFERS_APP
from docpool.base.content.archiving import IArchiving
from docpool.base.utils import get_content_area
from docpool.base.utils import getGroupsForCurrentUser
from docpool.elan.config import ELAN_APP
from docpool.rei.config import REI_APP
from plone import api
from plone.app.layout.navigation.interfaces import INavigationQueryBuilder
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.navtree import buildFolderTree
from plone.app.layout.viewlets import common
from plone.base.i18nl10n import utranslate
from plone.base.utils import safe_hasattr
from plone.memoize.view import memoize
from Products.CMFPlone.browser.navtree import DefaultNavtreeStrategy
from Products.CMFPlone.browser.navtree import SitemapQueryBuilder
from Products.PlonePAS.utils import cleanId
from zope.component import getMultiAdapter
from zope.globalrequest import getRequest
from zope.interface import implementer


caching_strategy = "anonymous"  # FIXME: maybe cache individually?


@implementer(INavigationQueryBuilder)
class DropDownMenuQueryBuilder(SitemapQueryBuilder):
    def __init__(self, context):
        super().__init__(context)
        self.context = context
        # customize depth according to dropdown menu settings
        if "depth" in self.query["path"]:
            self.query["path"]["depth"] = 4

        adaptQuery(self.query, context)
        # print self.query


@implementer(INavtreeStrategy)
class DropDownMenuStrategy(DefaultNavtreeStrategy):
    def __init__(self, context, view=None):
        super().__init__(context, view)
        self.bottomLevel = 0


class GlobalSectionsViewlet(common.GlobalSectionsViewlet):
    _item_markup_template_nolink = (
        '<li class="{id}{has_sub_class} nav-item">'
        '<a class="state-{review_state} nav-link"{aria_haspopup}>{title}</a>{opener}'  # noqa: E 501
        "{sub}"
        "</li>"
    )

    @property
    def _item_markup_template(self):
        class Wrapped:
            @staticmethod
            def format(**item):
                if item.get("url") is None:
                    return self._item_markup_template_nolink.format(**item)
                return common.GlobalSectionsViewlet._item_markup_template.format(**item)

        return Wrapped()

    @property
    @memoize
    def navtree(self):
        tree = super().navtree

        if api.user.is_anonymous():
            return tree

        self.navtree_add_apps_menu(tree)

        if not IArchiving(self.context).is_archive:
            self.navtree_add_contentarea(tree)

        # for tab in tree[self.navtree_path]:
        #     if "config" in tab["id"]:
        #         tab["item_class"] = "config"

        return tree

    portal_tabs = ()

    def customize_query(self, query):
        adaptQuery(query, self.context)

    def navtree_add_apps_menu(self, tree):
        current_dp, current_app, dp_apps = getApplicationDocPoolsForCurrentUser(
            self.context
        )
        app_title = appName(current_app) if current_app else None

        if current_dp:
            root_title = f"{current_dp.title}: {app_title}"
        else:
            root_title = utranslate("docpool.base", "Docpools", context=self.context)

        tree[self.navtree_path].insert(
            0,
            dict(
                id="apps",
                path=f"{self.navtree_path}/apps",
                uid="apps",
                title=root_title,
                review_state="visible",
                # item_class="applications",
            ),
        )

        apps_path = f"{self.navtree_path}/apps"
        current_dp_id = current_dp.getId() if current_dp else None

        for dp, app_names in dp_apps:
            dp_id = dp.getId()
            url = (self.context if current_dp_id == dp_id else dp).absolute_url()
            dp_path = f"{self.navtree_path}/apps/{dp_id}"
            tree[apps_path].append(
                dict(
                    id=dp_id,
                    path=dp_path,
                    uid=dp_id,
                    title=f"{dp.title}",
                    url=url,
                    review_state="visible",
                    # item_class=app_title,
                )
            )
            for app_title, app_name in sorted(
                {appName(i): i for i in app_names}.items()
            ):
                app_id = f"{dp_id}-{app_name}"
                tree[dp_path].append(
                    dict(
                        id=app_id,
                        path=f"{dp_path}/{app_name}",
                        uid=app_id,
                        title=f"{app_title}",
                        url=f"{url}/setActiveApp?app={app_name}",
                        review_state="visible",
                        # item_class=app_title,
                    )
                )

    def navtree_add_contentarea(self, tree):
        folders = getFoldersForCurrentUser(self.context)
        if not folders:
            return

        content_path = f"{self.navtree_path}/content"
        tree[self.navtree_path].append(
            dict(
                id="content",
                path=content_path,
                uid="content",
                title=utranslate("docpool.base", "Content Area", context=self.context),
                review_state="visible",
            )
        )

        tree[content_path] = []
        for folder in folders:
            self.recurse_folder(folder, content_path, tree)

    def recurse_folder(self, folder, parent_path, tree):
        path = folder["path"]
        tree[parent_path].append(
            dict(
                id=folder["id"],
                path=path,
                uid=folder["UID"],
                url=folder["getURL"],
                title=folder["Title"],
                review_state=folder["review_state"],
            )
        )
        tree[path] = []
        for child in folder.get("children", ()):
            self.recurse_folder(child, path, tree)


def adaptQuery(query, context):
    request = context.REQUEST
    dp_app_state = getMultiAdapter((context, request), name="dp_app_state")
    active_apps = dp_app_state.appsActivatedByCurrentUser()
    active_apps.extend([BASE_APP, TRANSFERS_APP])
    query["apps_supported"] = active_apps


def getApplicationDocPoolsForCurrentUser(context):
    """
    Determine all DocPools and their applications that the user has access to.
    """
    request = getRequest()

    dp_app_state = getMultiAdapter((context, request), name="dp_app_state")
    active_apps = dp_app_state.appsActivatedByCurrentUser()
    current_app = active_apps[0] if active_apps else None

    current_dp = None
    if safe_hasattr(context, "myDocumentPool"):
        current_dp = context.myDocumentPool()

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
        dp_app_state = getMultiAdapter((dp, request), name="dp_app_state")
        app_names = dp_app_state.appsAvailableToCurrentUser()

        if app_names:
            pools.append((dp, app_names))

    return current_dp, current_app, pools


def getFoldersForCurrentUser(context):
    """
    Additional navigation items for user folder and group folders.

    Results differ depending on user, state of the docpool and active app.
    """
    if api.user.is_anonymous():
        return

    user = api.user.get_current()

    content_area = get_content_area(context)
    if not content_area:
        return

    groups = getGroupsForCurrentUser(content_area, sort_on="getObjPositionInParent")
    if not groups:  # User is reader only
        return

    groups_folder = content_area["Groups"]
    groups_folder_path = "/".join(groups_folder.getPhysicalPath())
    # ELAN groups which can produce documents
    elan_groups = [group["id"] for group in groups if group["etypes"]]
    group_result = []
    for group_id in elan_groups:
        if groups_folder.get(group_id):
            gft = _folderTree(context, f"{groups_folder_path}/{group_id}")
            if "show_children" in gft:
                gft["item_class"] = "personal"
                group_result.append(gft)

    # show personal folder unless we're in elan or rei
    dp_app_state = getMultiAdapter((context, getRequest()), name="dp_app_state")
    effective_apps = dp_app_state.effectiveAppsHere()
    member_result = []
    if not effective_apps.intersection((ELAN_APP, REI_APP)):
        members_folder = content_area["Members"]
        members_folder_path = "/".join(members_folder.getPhysicalPath())
        # member folders for users with '-' in their username are created with double dashes
        user_name = cleanId(user.getUserName())
        member_tree = _folderTree(context, f"{members_folder_path}/{user_name}")
        # A folder for the user has not been found, e.g. in archive
        if "show_children" in member_tree:
            member_tree["item_class"] = "personal"
            member_result = [member_tree]

    if elan_groups and not group_result:
        # If the groups are not navigable (i.e. in archive): only member folder
        return member_result

    transfers_result = []
    roles = api.user.get_roles(user=user, obj=context)
    if (
        "Manager" in roles
        or "Site Administrator" in roles
        or any(("Receivers" in group["id"]) for group in groups)
    ):
        transfers = content_area.get("Transfers")
        if transfers:
            path = "/".join(transfers.getPhysicalPath())
            transfers_tree = _folderTree(context, path)
            transfers_tree["item_class"] = "personal transfer"
            transfers_result = [transfers_tree]

    if group_result:
        # Has groups, so return all the folders
        return transfers_result + member_result + group_result
    # otherwise this will be empty for a reading user, or the Transfers for a receiver
    return transfers_result


def _folderTree(context, path, filter={}):
    """Return tree of tabs based on content structure"""

    queryBuilder = DropDownMenuQueryBuilder(context)
    query = queryBuilder()
    query.update(filter)
    query["path"] = {"query": path, "depth": 1, "navtree": 1, "navtree_start": 2}
    strategy = getMultiAdapter((context, None), INavtreeStrategy)
    strategy.rootPath = path
    return buildFolderTree(context, obj=context, query=query, strategy=strategy)
