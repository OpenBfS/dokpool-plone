from docpool.base.config import BASE_APP
from docpool.base.utils import getDocumentPoolSite, getGroupsForCurrentUser
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

        pools.append((dp, app_names))

    return current_dp, current_app, pools


def getFoldersForCurrentUser(context):
    """
    Additional navigation-items for user-folder and group-folders.

    Results differ depending on user, state of the docpool and active app.
    example = [{
        'Creator': 'user1',
        'Description': '',
        'Title': 'user1 (Bund)',
        'UID': '8dd836f9ff474897a8e618cf019c73a4',
        'absolute_url': 'http://localhost:8081/Plone6/bund/content/Members/user1',
        'children': [],
        'creation_date': '2019-10-07T16:17:51+02:00',
        'currentItem': False,
        'currentParent': False,
        'depth': 0,
        'getRemoteUrl': Missing.Value,
        'getURL': 'http://localhost:8081/Plone6/bund/content/Members/user1',
        'id': 'user1',
        'item': <Products.ZCatalog.Catalog.mybrains object at 0x10e109460>,
        'item_class': 'personal',
        'link_remote': Missing.Value,
        'no_display': False,
        'normalized_id': 'user1',
        'normalized_portal_type': 'userfolder',
        'normalized_review_state': 'published',
        'path': '/Plone6/bund/content/Members/user1',
        'portal_type': 'UserFolder',
        'review_state': 'published',
        'show_children': True,
        'useRemoteUrl': False,
    }, {
        'Creator': 'admin',
        'Description': '',
        'Title': 'Group1 (Bund)',
        'UID': '4001a95e06394747aa6d697addf50065',
        'absolute_url': 'http://localhost:8081/Plone6/bund/content/Groups/bund_group1',
        'children': [],
        'creation_date': '2019-09-28T11:43:00+02:00',
        'currentItem': False,
        'currentParent': False,
        'depth': 0,
        'getRemoteUrl': Missing.Value,
        'getURL': 'http://localhost:8081/Plone6/bund/content/Groups/bund_group1',
        'id': 'bund_group1',
        'item': <Products.ZCatalog.Catalog.mybrains object at 0x10df640b8>,
        'item_class': 'personal',
        'link_remote': Missing.Value,
        'no_display': False,
        'normalized_id': 'bund_group1',
        'normalized_portal_type': 'groupfolder',
        'normalized_review_state': 'published',
        'path': '/Plone6/bund/content/Groups/bund_group1',
        'portal_type': 'GroupFolder',
        'review_state': 'published',
        'show_children': True,
        'useRemoteUrl': False,
    }]
    """
    if api.user.is_anonymous():
        return None
    user = api.user.get_current()
    res = []
    if getattr(context, "myDocumentPool", None) is None:
        return res
    docpool = getDocumentPoolSite(context)
    content_folder = docpool.get("content")
    if not content_folder:
        return res
    rres = []
    groups = getGroupsForCurrentUser(context, user)
    if not groups:  # User is reader only
        return rres

    user_is_receiver = False
    roles = api.user.get_roles(user=user, obj=context)
    if "Manager" in roles or "Site Administrator" in roles:
        user_is_receiver = True
    elif any([("Receivers" in group["id"]) for group in groups]):
        user_is_receiver = True
    if user_is_receiver:
        # add the transfers folder if it exists.
        transfers = content_folder.get("Transfers")
        if transfers:
            path = "/".join(transfers.getPhysicalPath())
            rres = [
                _folderTree(
                    context,
                    path,
                )
            ]
            rres[0]["item_class"] = "personal transfer"

    # strangely, member folders for users with '-' in their username
    # are created with double dashes
    user_name = user.getUserName().replace("-", "--")
    members_folder = content_folder["Members"]
    groups_folder = content_folder["Groups"]
    members_folder_path = "/".join(members_folder.getPhysicalPath())
    groups_folder_path = "/".join(groups_folder.getPhysicalPath())

    has_group = False
    group_result = []
    for group in groups:
        if group["etypes"]:
            # Group is ELAN group which can produce documents
            has_group = True
            if groups_folder.get(group["id"]):
                gft = _folderTree(
                    context,
                    "{}/{}".format(groups_folder_path, group["id"]),
                )
                # print gft
                if "show_children" in gft:
                    gft["item_class"] = "personal"
                    group_result.append(gft)
    res.extend(group_result)

    # show personal folder unless we're in elan
    dp_app_state = getMultiAdapter((context, context.REQUEST), name="dp_app_state")
    effective_apps = dp_app_state.effectiveAppsHere()
    hide_user_folder = "elan" in effective_apps or "rei" in effective_apps
    member_result = []
    if not hide_user_folder:
        member_result = [
            _folderTree(
                context,
                f"{members_folder_path}/{user_name}",
            )
        ]
        # A folder for the user has not been found, e.g. in archive
        if member_result and "show_children" not in member_result[0]:
            # print "has no user folder"
            member_result = []
        else:
            member_result[0]["item_class"] = "personal"
        res.extend(member_result)

    res.extend(rres)
    res.reverse()
    if group_result:
        # Has groups, so return all the folders
        return res
    if has_group:
        # If the groups are not navigable (i.e. in archive): only member folder
        return member_result
    # otherwise this will be empty for a reading user, or the Transfers for a receiver
    return rres


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
