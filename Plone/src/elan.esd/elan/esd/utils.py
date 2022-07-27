from docpool.base.utils import getDocumentPoolSite
from plone import api


def getAvailableCategories(self):
    esd = getDocumentPoolSite(self)
    path = "/".join(esd.getPhysicalPath()) + "/esd"
    brains = api.content.find(
        path=path,
        portal_type="ELANDocCollection",
        dp_type=["active"],
        sort_on="sortable_title",
    )
    return [i for i in brains if i.id not in ["recent", "overview"]]


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
