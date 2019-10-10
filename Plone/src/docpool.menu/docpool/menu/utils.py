from docpool.base.appregistry import appName
from docpool.base.config import BASE_APP
from docpool.base.utils import getDocumentPoolSite
from docpool.base.utils import getGroupsForCurrentUser
from docpool.base.utils import queryForObjects
from docpool.transfers.config import TRANSFERS_APP
from plone import api
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.navtree import buildFolderTree
from Products.CMFPlone.utils import safe_hasattr
from Products.CMFPlone.i18nl10n import utranslate
from zope.component import getMultiAdapter
from zope.site.hooks import getSite


def getApplicationDocPoolsForCurrentUser(context, user=None):
    """
    Determine all accessible DocPools an their applications, that the user has access to.
    """
    if not user:
        if api.user.is_anonymous():
            return None
        user = api.user.get_current()

    portal = getSite()

    dps = [
        dp.getObject()
        for dp in queryForObjects(
            context, path="/".join(portal.getPhysicalPath()), portal_type='DocumentPool'
        )
    ]

    # dps = _folderTree(context, "%s" % ("/".join(portal.getPhysicalPath())), {'portal_type': ('PloneSite', 'DocumentPool')})['children']
    request = context.REQUEST
    dp_app_state = getMultiAdapter((context, request), name=u'dp_app_state')
    active_apps = dp_app_state.appsActivatedByCurrentUser()
    current_app = None
    if len(active_apps) > 0:
        current_app = appName(active_apps[0])
    current_dp = None
    if safe_hasattr(context, "myDocumentPool"):
        current_dp = context.myDocumentPool()
    root_title = (
        current_dp is None
        and utranslate("docpool.menu", "Docpools", context=context)
        or "%s: %s" % (current_dp.Title(), current_app)
    )
    apps_root = [
        {
            'id': 'apps',
            'Title': root_title,
            'Description': '',
            'getURL': '',
            'show_children': True,
            'children': None,
            'currentItem': False,
            'currentParent': True,
            'item_class': 'applications',
            'normalized_review_state': 'visible',
        }
    ]
    pools = []
    for dp in dps:
        dp_app_state = getMultiAdapter(
            (dp, request), name=u'dp_app_state'
        )  # need to get fresh adapter for each pool
        app_names = dp_app_state.appsAvailableToCurrentUser()
        app_names.insert(0, BASE_APP)
        for app_name in app_names:
            if app_name == 'base':
                if context.isAdmin():
                    app_title = utranslate(
                        "docpool.menu", "Docpool Base", context=context)
                else:
                    continue
            else:
                app_title = appName(app_name)

            if dp.getId() in context.absolute_url():
                pools.append(
                    {
                        'id': dp.getId() + "-" + app_name,
                        'Title': dp.Title() + ": " + app_title,
                        'Description': '',
                        'getURL': "%s/setActiveApp?app=%s"
                        % (context.absolute_url(), app_name),
                        'show_children': False,
                        'children': [],
                        'currentItem': False,
                        'currentParent': False,
                        'item_class': app_title,
                        'normalized_review_state': 'visible',
                    }
                )
            else:
                pools.append(
                    {
                        'id': dp.getId() + "-" + app_name,
                        'Title': dp.Title() + ": " + app_title,
                        'Description': '',
                        'getURL': "%s/setActiveApp?app=%s"
                        % (dp.absolute_url(), app_name),
                        'show_children': False,
                        'children': [],
                        'currentItem': False,
                        'currentParent': False,
                        'item_class': app_title,
                        'normalized_review_state': 'visible',
                    }
                )

    apps_root[0]['children'] = pools
    return apps_root


def getFoldersForCurrentUser(
        context, user=None, queryBuilderClass=None, strategy=None):
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
    if not user:
        if api.user.is_anonymous():
            return None
        user = api.user.get_current()
    res = []
    if getattr(context, 'myDocumentPool', None) is None:
        return res
    docpool = getDocumentPoolSite(context)
    content_folder = docpool.get('content')
    if not content_folder:
        return res
    rres = []
    groups = getGroupsForCurrentUser(context, user)
    if not groups:  # User is reader only
        return rres

    user_is_receiver = False
    roles = api.user.get_roles(user=user, obj=context)
    if 'Manager' in roles or 'Site Administrator' in roles:
        user_is_receiver = True
    elif any([('Receivers'in group['id']) for group in groups]):
        user_is_receiver = True
    if user_is_receiver:
        # add the transfers folder if it exists.
        transfers = content_folder.get('Transfers')
        if transfers:
            path = '/'.join(transfers.getPhysicalPath())
            rres = [
                _folderTree(
                    context,
                    path,
                    queryBuilderClass=queryBuilderClass,
                    strategy=strategy,
                )
            ]
            rres[0]['item_class'] = 'personal transfer'

    # strangely, member folders for users with '-' in their username
    # are created with double dashes
    user_name = user.getUserName().replace("-", "--")
    members_folder = content_folder['Members']
    groups_folder = content_folder['Groups']
    members_folder_path = '/'.join(members_folder.getPhysicalPath())
    groups_folder_path = '/'.join(groups_folder.getPhysicalPath())

    has_group = False
    group_result = []
    for group in groups:
        if group['etypes']:
            # Group is ELAN group which can produce documents
            has_group = True
            if groups_folder.get(group['id']):
                gft = _folderTree(
                    context,
                    "%s/%s" % (groups_folder_path, group['id']),
                    queryBuilderClass=queryBuilderClass,
                    strategy=strategy,
                )
                # print gft
                if "show_children" in gft:
                    gft['item_class'] = "personal"
                    group_result.append(gft)
    res.extend(group_result)
    member_result = [
        _folderTree(
            context,
            "%s/%s" % (members_folder_path, user_name),
            queryBuilderClass=queryBuilderClass,
            strategy=strategy,
        )
    ]
    # A folder for the user has not been found, e.g. in archive
    if member_result and "show_children" not in member_result[0]:
        # print "has no user folder"
        member_result = []
    else:
        member_result[0]['item_class'] = "personal"
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


def _folderTree(context, path, filter={},
                queryBuilderClass=None, strategy=None):
    """Return tree of tabs based on content structure"""

    from docpool.menu.browser.menu import DropDownMenuQueryBuilder

    if not queryBuilderClass:
        queryBuilder = DropDownMenuQueryBuilder(context)
        query = queryBuilder()
        query.update(filter)
        query['path'] = {
            'query': path,
            'depth': 1,
            'navtree': 1,
            'navtree_start': 2}
    else:
        queryBuilder = queryBuilderClass(context)
        query = queryBuilder()
        query['path'] = {
            'query': path,
            'depth': 1,
            'navtree': 1,
            'navtree_start': 2}
    if not strategy:
        strategy = getMultiAdapter((context, None), INavtreeStrategy)
    strategy.rootPath = path
    return buildFolderTree(context, obj=context,
                           query=query, strategy=strategy)


def adaptQuery(query, context):
    request = context.REQUEST
    dp_app_state = getMultiAdapter((context, request), name=u'dp_app_state')
    active_apps = dp_app_state.appsActivatedByCurrentUser()
    active_apps.extend([BASE_APP, TRANSFERS_APP])
    query['apps_supported'] = active_apps
