from Products.CMFCore.utils import getToolByName
from Acquisition import aq_inner
from Products.Archetypes.utils import shasattr
from Products.CMFPlone.log import log_exc
from zope.component import getUtility
from zope.intid.interfaces import IIntIds
from zope.security import checkPermission
from zc.relation.interfaces import ICatalog
from Products.CMFPlone.utils import parent
from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager, setSecurityManager
from AccessControl.User import UnrestrictedUser as BaseUnrestrictedUser
from zope.component.hooks import getSite
from plone import api
from docpool.base.utils import getDocumentPoolSite, getGroupsForCurrentUser
from docpool.elan.config import ELAN_APP


def getAvailableCategories(self):
    cat = getToolByName(self, "portal_catalog")
    esd = getDocumentPoolSite(self)
    res0 = cat(path="/".join(esd.getPhysicalPath()) + "/esd", portal_type = 'ELANDocCollection', dp_type=["active"], sort_on="sortable_title")
    res = []
    for r in res0:
      if r.id not in ["recent","overview"]:
        res.append(r)
    return res


def getCategoriesForCurrentUser(self):
    user = api.user.get_current()
    cs = user.getProperty("categories", None)
    if not cs:
        return []
    return list(cs)

def setCategoriesForCurrentUser(self, cats):
    """
    """
    if type(cats) == type(""):
        cats = [cats]
    user = api.user.get_current()
    user.setMemberProperties({"categories": cats})


def getRelativePath(obj):
    if obj.isArchive():
        portal_path_length = len( obj.myELANArchive().getPhysicalPath() )
        content_path = obj.getPhysicalPath()
        return "/".join(content_path[portal_path_length:])
    else:
        # print obj
        # print obj.portal_url()
        # print obj.portal_url.getRelativeUrl(obj)
        return obj.portal_url.getRelativeUrl(obj)
    
def isElanEsdInstalled(self):
    """
    """
    qi = getToolByName(self, 'portal_quickinstaller')
    prods = qi.listInstallableProducts(skipInstalled=False)
    for prod in prods:
        if (prod['id'] == 'elan.esd') and (prod['status'] == 'installed'):
            return 1
    return 0

