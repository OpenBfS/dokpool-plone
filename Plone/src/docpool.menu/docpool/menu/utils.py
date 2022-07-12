from docpool.base.config import BASE_APP
from docpool.base.utils import getGroupsForCurrentUser
from docpool.elan.config import ELAN_APP
from docpool.rei.config import REI_APP
from docpool.transfers.config import TRANSFERS_APP
from plone import api
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.navtree import buildFolderTree
from Products.CMFPlone.utils import safe_hasattr
from zope.component import getMultiAdapter
from zope.globalrequest import getRequest


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
        if context.isAdmin():
            app_names.insert(0, BASE_APP)

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

    if not safe_hasattr(context, "myDocumentPool"):
        return

    docpool = context.myDocumentPool()
    content_folder = docpool.get("content")
    if not content_folder:
        return

    groups = getGroupsForCurrentUser(context)
    if not groups:  # User is reader only
        return

    groups_folder = content_folder["Groups"]
    groups_folder_path = "/".join(groups_folder.getPhysicalPath())
    has_group = False
    group_result = []
    for group in groups:
        if group["etypes"]:
            # Group is ELAN group which can produce documents
            has_group = True
            if groups_folder.get(group["id"]):
                gft = _folderTree(context, f"{groups_folder_path}/{group['id']}")
                if "show_children" in gft:
                    gft["item_class"] = "personal"
                    group_result.append(gft)
    group_result.reverse()

    # show personal folder unless we're in elan or rei
    dp_app_state = getMultiAdapter((context, getRequest()), name="dp_app_state")
    effective_apps = dp_app_state.effectiveAppsHere()
    member_result = []
    if not effective_apps.intersection((ELAN_APP, REI_APP)):
        # strangely, member folders for users with '-' in their username
        # are created with double dashes
        user_name = user.getUserName().replace("-", "--")
        members_folder = content_folder["Members"]
        members_folder_path = "/".join(members_folder.getPhysicalPath())
        member_tree = _folderTree(context, f"{members_folder_path}/{user_name}")
        # A folder for the user has not been found, e.g. in archive
        if "show_children" in member_tree:
            member_tree["item_class"] = "personal"
            member_result = [member_tree]

    if has_group and not group_result:
        # If the groups are not navigable (i.e. in archive): only member folder
        return member_result

    transfers_result = []
    roles = api.user.get_roles(user=user, obj=context)
    if (
        "Manager" in roles
        or "Site Administrator" in roles
        or any(("Receivers" in group["id"]) for group in groups)
    ):
        transfers = content_folder.get("Transfers")
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

    from docpool.menu.browser.menu import DropDownMenuQueryBuilder

    queryBuilder = DropDownMenuQueryBuilder(context)
    query = queryBuilder()
    query.update(filter)
    query["path"] = {"query": path, "depth": 1, "navtree": 1, "navtree_start": 2}
    strategy = getMultiAdapter((context, None), INavtreeStrategy)
    strategy.rootPath = path
    return buildFolderTree(context, obj=context, query=query, strategy=strategy)


def adaptQuery(query, context):
    request = context.REQUEST
    dp_app_state = getMultiAdapter((context, request), name="dp_app_state")
    active_apps = dp_app_state.appsActivatedByCurrentUser()
    active_apps.extend([BASE_APP, TRANSFERS_APP])
    query["apps_supported"] = active_apps
