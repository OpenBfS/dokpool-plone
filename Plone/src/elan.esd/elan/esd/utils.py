from docpool.base.utils import getDocumentPoolSite
from plone import api
from Products.CMFCore.utils import getToolByName


def getAvailableCategories(self):
    cat = getToolByName(self, "portal_catalog")
    esd = getDocumentPoolSite(self)
    res0 = cat(
        path="/".join(esd.getPhysicalPath()) + "/esd",
        portal_type='ELANDocCollection',
        dp_type=["active"],
        sort_on="sortable_title",
    )
    res = []
    for r in res0:
        if r.id not in ["recent", "overview"]:
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
    if isinstance(cats, type("")):
        cats = [cats]
    user = api.user.get_current()
    user.setMemberProperties({"categories": cats})


def getRelativePath(obj):
    if obj.restrictedTraverse("@@context_helpers").is_archive():
        portal_path_length = len(obj.myELANArchive().getPhysicalPath())
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
