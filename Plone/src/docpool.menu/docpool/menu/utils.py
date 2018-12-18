from Products.CMFCore.utils import getToolByName
from Products.Archetypes.utils import shasattr

from docpool.base.appregistry import appName
from docpool.base.utils import getGroupsForCurrentUser, queryForObjects
from zope.component import getMultiAdapter
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.navtree import buildFolderTree
from plone import api
from zope.site.hooks import getSite
from Products.CMFPlone.i18nl10n import utranslate
from docpool.base.config import BASE_APP
from docpool.transfers.config import TRANSFERS_APP

def getApplicationDocPoolsForCurrentUser(self, user=None):
    """
    Determine all accessible DocPools an their applications, that the user has access to.
    """
    if not user:
        if api.user.is_anonymous():
            return None
        user = api.user.get_current()
    
    portal = getSite()

    dps = [ dp.getObject() for dp in queryForObjects(self, path = "/".join(portal.getPhysicalPath()), portal_type='DocumentPool') ]

    #dps = _folderTree(self, "%s" % ("/".join(portal.getPhysicalPath())), {'portal_type': ('PloneSite', 'DocumentPool')})['children']
    request = self.REQUEST
    dp_app_state = getMultiAdapter((self, request), name=u'dp_app_state')
    active_apps = dp_app_state.appsActivatedByCurrentUser()
    current_app = None
    if len(active_apps) > 0:
        current_app = appName(active_apps[0])
    current_dp = None
    if shasattr(self, "myDocumentPool", True):
        current_dp = self.myDocumentPool()
    root_title = current_dp is None and utranslate("docpool.menu", "Docpools", context=self) or "%s: %s" % (current_dp.Title(), current_app)
    apps_root = [ 
                    {'id': 'apps',
                     'Title': root_title,
                     'Description': '',
                     'getURL': '',
                     'show_children': True,
                     'children': None,
                     'currentItem': False,
                     'currentParent': True,
                     'item_class': 'applications',
                     'normalized_review_state': 'visible'}
            
             ]
    pools = []
    for dp in dps:
        apps = [] # determine locally available apps
        dp_app_state = getMultiAdapter((dp, request), name=u'dp_app_state') # need to get fresh adapter for each pool
        app_names = dp_app_state.appsAvailableToCurrentUser()
        app_names.insert(0, BASE_APP)
        for app_name in app_names:
            if app_name == 'base':
                if self.isAdmin():
                    app_title = utranslate("docpool.menu", "Docpool Base", context=self)
                else:
                    continue
            else:
                app_title = appName(app_name)

            if dp.getId() in self.absolute_url():
               pools.append({'id': dp.getId() + "-" + app_name,
                        'Title': dp.Title() + ": " + app_title,
                        'Description': '',
                        'getURL': "%s/setActiveApp?app=%s" % (self.absolute_url(), app_name),
                        'show_children': False,
                        'children': [],
                        'currentItem': False,
                        'currentParent': False,
                        'item_class': app_title,
                        'normalized_review_state': 'visible'})
            else:
               pools.append({'id': dp.getId() + "-" + app_name,
                        'Title': dp.Title() + ": " + app_title,
                        'Description': '',
                        'getURL': "%s/setActiveApp?app=%s" % (dp.absolute_url(), app_name),
                        'show_children': False,
                        'children': [],
                        'currentItem': False,
                        'currentParent': False,
                        'item_class': app_title,
                        'normalized_review_state': 'visible'})


    apps_root[0]['children'] = pools
    return apps_root

    
def getFoldersForCurrentUser(self, user=None, queryBuilderClass=None, strategy=None):
    """
    example = {'getURL': 'http://localhost:8081/Plone/basics', 'Title': 'Basics', 'creation_date': '2012-06-28T16:31:29+02:00', 'item_icon': None, 'id': 'basics', 'no_display': False, 'show_children': True, 'UID': '00a874166069411189bbc0c86c9caab7', 'normalized_review_state': 'published', 'depth': 1, 'children': [], 'currentItem': False, 'review_state': 'published', 'getRemoteUrl': None, 'portal_type': 'Folder', 'path': '/Plone/basics', 'Description': '', 'useRemoteUrl': False, 'normalized_id': 'basics', 'normalized_portal_type': 'folder', 'Creator': 'admin', 'absolute_url': 'http://localhost:8081/Plone/basics', 'item': None, 'currentParent': False, 'link_remote': None}
    """
    if not user:
        if api.user.is_anonymous():
            return None
        user = api.user.get_current()
    res = []
    if not shasattr(self, "content", True):
        return res
    rres = []
    # FIXME: this code knows about a specific application
    if self.isReceiver():
        if hasattr(self.content, "Transfers"):
            t = self.content.Transfers
            tpath = "/".join(t.getPhysicalPath())
            rres = [ _folderTree(self, "%s" % (tpath), queryBuilderClass=queryBuilderClass, strategy=strategy)]
            rres[0]['item_class'] = 'personal transfer'
    groups = getGroupsForCurrentUser(self, user)
    if not groups: # User is reader only
        return rres
    # strangely, member folders for users with '-' in their username 
    # are created with double dashes
    user_name = user.getUserName()
    user_name = user_name.replace("-", "--")
    m = self.content.Members
    g = self.content.Groups
    mpath = "/".join(m.getPhysicalPath())
    gpath = "/".join(g.getPhysicalPath())
    hasGroup = False
    gres = []
    for group in groups:
        if group['etypes']: # Group is ELAN group which can produce documents
            hasGroup = True
#            print group, "isELAN"
            if shasattr(g, group['id']): # only when the folder really exists
#                print "exists"
                gft = _folderTree(self, "%s/%s" % (gpath, group['id']), queryBuilderClass=queryBuilderClass, strategy=strategy)
#                print gft
                if gft.has_key("show_children"):
                    gft['item_class'] = "personal"
                    gres.append(gft)
    res.extend(gres)
    mfolder = [ _folderTree(self, "%s/%s" % (mpath,user_name), queryBuilderClass=queryBuilderClass, strategy=strategy) ]
    if mfolder and not mfolder[0].has_key("show_children"): # A folder for the user has not been found, e.g. in archive
#        print "has no user folder"
        mfolder = []
    else:
        mfolder[0]['item_class'] = "personal"
    res.extend(mfolder)
    res.extend(rres)
    res.reverse()
    if gres: # Has groups, so return all the folders
        return res
    elif hasGroup: # If the groups are not navigable (i.e. in archive): only member folder
        return mfolder
    return rres # otherwise this will be empty for a reading user, or the Transfers for a receiver
# 
# def deleteMemberFolders(self, member_ids):
#     """
#     """
#     for mid in member_ids:
#         try:
#             # TODO
#             self.portal_membership.getMembersFolder().manage_delObjects([mid.replace("-","--")])
#         except Exception, e:
#             log_exc(e)



def _folderTree(context, path, filter={}, queryBuilderClass=None, strategy=None):
    """Return tree of tabs based on content structure"""

    from docpool.menu.browser.menu import DropDownMenuQueryBuilder
    if not queryBuilderClass:
        queryBuilder = DropDownMenuQueryBuilder(context)
        query = queryBuilder()
        query.update(filter)
        query['path'] = {'query': path, 'depth': 1, 'navtree': 1, 'navtree_start': 2}
    else:
        queryBuilder = queryBuilderClass(context)
        query = queryBuilder()
        query['path'] = {'query': path, 'depth': 1, 'navtree': 1, 'navtree_start': 2}
    if not strategy:
        strategy = getMultiAdapter((context, None), INavtreeStrategy)
    strategy.rootPath = path
    return buildFolderTree(context, obj=context, query=query,
                           strategy=strategy)

def adaptQuery(query, context):
    request = context.REQUEST
    dp_app_state = getMultiAdapter((context, request), name=u'dp_app_state')
    active_apps = dp_app_state.appsActivatedByCurrentUser()
    active_apps.extend([BASE_APP, TRANSFERS_APP])
    query['apps_supported'] = active_apps
