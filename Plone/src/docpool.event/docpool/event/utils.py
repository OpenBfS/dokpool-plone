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


def getActiveScenarios(self):
    cat = getToolByName(self, "portal_catalog")
    esd = getDocumentPoolSite(self)
    res = cat(
        path="/".join(esd.getPhysicalPath()) + "/contentconfig",
        portal_type='DPEvent',
        dp_type="active",
        sort_on="modified",
        sort_order="reverse",
    )
    return res


def getOpenScenarios(self):
    cat = getToolByName(self, "portal_catalog")
    esd = getDocumentPoolSite(self)
    res = cat(
        path="/".join(esd.getPhysicalPath()) + "/contentconfig",
        portal_type='DPEvent',
        dp_type=["active", "inactive"],
        sort_on="created",
        sort_order="reverse",
    )
    return res


def getScenariosForCurrentUser(self):
    """
    """
    mtool = getToolByName(self, "portal_membership")
    user = mtool.getAuthenticatedMember()
    sc = user.getProperty("scenarios", None)
    if not sc:
        # intented implementation: use the latest active scenario
        # a_s = getActiveScenarios(self)
        # sc = len(a_s) > 0 and [ a_s[0].Title ] or []
        # temporarily: no filter
        return []
    return list(sc)


def setScenariosForCurrentUser(self, scenarios):
    """
    """
    user = api.user.get_current()
    user.setMemberProperties({"scenarios": scenarios})
