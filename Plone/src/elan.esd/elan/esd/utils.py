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


def getActiveScenarios(self):
    cat = getToolByName(self, "portal_catalog")
    esd = getDocumentPoolSite(self)
    res = cat(path="/".join(esd.getPhysicalPath()) + "/contentconfig", portal_type = 'ELANScenario', dp_type="active", sort_on="modified", sort_order="reverse")
    return res

def getOpenScenarios(self):
    cat = getToolByName(self, "portal_catalog")
    esd = getDocumentPoolSite(self)
    res = cat(path="/".join(esd.getPhysicalPath()) + "/contentconfig", portal_type = 'ELANScenario', dp_type=["active","inactive"], sort_on="created", sort_order="reverse")
    return res

def getAvailableCategories(self):
    cat = getToolByName(self, "portal_catalog")
    esd = getDocumentPoolSite(self)
    res = cat(path="/".join(esd.getPhysicalPath()) + "/esd", portal_type = 'ELANDocCollection', dp_type=["active"], sort_on="sortable_title")
    return res

def getScenariosForCurrentUser(self):
    """
    """
    mtool = getToolByName(self, "portal_membership")
    user = mtool.getAuthenticatedMember()
    sc = user.getProperty("scenarios", None)
    if not sc:
        # intented implementation: use the latest active scenario
        #a_s = getActiveScenarios(self)
        #sc = len(a_s) > 0 and [ a_s[0].Title ] or []
        # temporarily: no filter
        return []
    return list(sc)

def getCategoriesForCurrentUser(self):
    user = api.user.get_current()
    cs = user.getProperty("categories", None)
    if not cs:
        return []
    return list(cs)

def setScenariosForCurrentUser(self, scenarios):
    """
    """
    user = api.user.get_current()
    user.setMemberProperties({"scenarios": scenarios})
    
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

