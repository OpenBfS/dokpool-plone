from docpool.base.utils import getDocumentPoolSite
from plone import api
from Products.CMFCore.utils import getToolByName


def getAvailableCategories(self):
    cat = getToolByName(self, "portal_catalog")
    esd = getDocumentPoolSite(self)
    res0 = cat(
        path="/".join(esd.getPhysicalPath()) + "/esd",
        portal_type="ELANDocCollection",
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
    """ """
    if isinstance(cats, str):
        cats = [cats]
    user = api.user.get_current()
    user.setMemberProperties({"categories": cats})
