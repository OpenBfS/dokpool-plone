from Products.CMFCore.utils import getToolByName
from Products.Archetypes.utils import shasattr
from docpool.base.utils import getGroupsForCurrentUser
from docpool.menu.browser.menu import DropDownMenuQueryBuilder
from zope.component import getMultiAdapter
from plone.app.layout.navigation.interfaces import INavtreeStrategy
from plone.app.layout.navigation.navtree import buildFolderTree
from plone import api
from zope.site.hooks import getSite
from Products.CMFPlone.i18nl10n import utranslate

def getApplicationDocPoolsForCurrentUser(self, user=None):
    """
    Determine all accessible DocPools in all applications, that the user has access to.
    TODO: multiple applications are not yet implemented.
    """
    if not user:
        if api.user.is_anonymous():
            return None
        user = api.user.get_current()
    
    portal = getSite()
        
    username = user.getUserName()
    parts = username.split("_")
    dp_prefix = parts[0]
    dps = _folderTree(self, "%s" % ("/".join(portal.getPhysicalPath())), {'portal_type': ('PloneSite', 'DocumentPool')})['children']
    current_app = 'ELAN' #TODO:
    current_dp = None
    if shasattr(self, "myDocumentPool", True):
        current_dp = self.myDocumentPool()
    root_title = current_dp is None and utranslate("docpool.menu", "Applications", context=self) or "%s: %s" % (current_app, current_dp.Title())
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
    apps = []
    for app in [ 'ELAN' ]: #TODO:
        app_root = {'id': app.lower(),
                     'Title': utranslate("docpool.menu", app, context=self),
                     'Description': '',
                     'getURL': '',
                     'show_children': True,
                     'children': dps,
                     'currentItem': False,
                     'currentParent': True,
                     'item_class': app.lower(),
                     'normalized_review_state': 'visible'}
        apps.append(app_root)
        
    apps_root[0]['children'] = apps
    return apps_root

    
def getFoldersForCurrentUser(self, user=None):
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
    if self.isReceiver():
        t = self.content.Transfers
        tpath = "/".join(t.getPhysicalPath())
        rres = [ _folderTree(self, "%s" % (tpath))]
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
                gft = _folderTree(self, "%s/%s" % (gpath, group['id']))
#                print gft
                if gft.has_key("show_children"):
                    gres.append(gft)
    res.extend(gres)
    mfolder = [ _folderTree(self, "%s/%s" % (mpath,user_name)) ]
    if mfolder and not mfolder[0].has_key("show_children"): # A folder for the user has not been found, e.g. in archive
#        print "has no user folder"
        mfolder = []
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



def _folderTree(context, path, filter={}):
    """Return tree of tabs based on content structure"""

    queryBuilder = DropDownMenuQueryBuilder(context)
    strategy = getMultiAdapter((context, None), INavtreeStrategy)
    strategy.rootPath = path
    query = queryBuilder()
    query.update(filter)
    query['path'] = {'query': path, 'depth': 3, 'navtree' : 1, 'navtree_start' : 2}
    return buildFolderTree(context, obj=context, query=query,
                           strategy=strategy)
