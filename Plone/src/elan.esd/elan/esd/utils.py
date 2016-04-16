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

# def queryForObject(self, **kwa):
#     """
#     """
#     cat = getToolByName(self, "portal_catalog")
#     # print kwa
#     res = cat(kwa)
#     if len(res) == 1:
#         return res[0].getObject()
#     else:
#         return None
# 
# def queryForObjects(self, **kwa):
#     """
#     """
#     cat = getToolByName(self, "portal_catalog")
#     #print kwa
#     res = cat(kwa)
#     return res
#     
# def getAllowedELANDocumentTypes(self):
#     """
#     Determine the ELAN document types allowed for the current user in the current context
#     """
#     # if in a group folder, only allow the types for this group
#     isGF = self.isGroupFolder()
#         
#     grps = getGroupsForCurrentUser(self)
#     dts = []
#     # Determine the union of the allowed documents for each of the user's groups
#     if grps:
#         for grp in grps:
#             if not isGF or grp['id'] in self.getPhysicalPath():
#                 dts.extend(grp['etypes'])
#     tids = list(set(dts))
#     cat = getToolByName(self, "portal_catalog")
#     esd = getDocumentPoolSite(self)
#     res = cat(path="/".join(esd.getPhysicalPath()) + "/config", portal_type = 'DocType', id=tids, sort_on="sortable_title")
#     return res
# 
# def getAllowedELANDocumentTypesForGroup(self):
#     """
#     """
#     isGF = self.isGroupFolder()
#     dts = []
#     if isGF:
#         grp = self.getGroupOfFolder()
#         dts.extend(grp.getProperty('allowedDocTypes', []))
#     else:
#         return getAllowedELANDocumentTypes(self)
#     tids = list(set(dts))
#     cat = getToolByName(self, "portal_catalog")
#     esd = getDocumentPoolSite(self)
#     res = cat(path="/".join(esd.getPhysicalPath()) + "/config", portal_type = 'DocType', id=tids, sort_on="sortable_title")
#     return res

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
    mtool = getToolByName(self, "portal_membership")
    user = mtool.getAuthenticatedMember()
    cs = user.getProperty("categories", None)
    if not cs:
        return []
    return list(cs)

def setScenariosForCurrentUser(self, scenarios):
    """
    """
    mtool = getToolByName(self, "portal_membership")
    user = mtool.getAuthenticatedMember()
    user.setMemberProperties({"scenarios": scenarios})
    
def setCategoriesForCurrentUser(self, cats):
    """
    """
    if type(cats) == type(""):
        cats = [cats]
    mtool = getToolByName(self, "portal_membership")
    user = mtool.getAuthenticatedMember()
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

def getTupleForTransfer(self, id):
    """
    """
    from elan.esd.behaviors.elandocument import IELANDocument
    doc = self._getOb(id)
    return doc, IELANDocument(doc)
