from docpool.elan.utils import getScenariosForCurrentUser
from Products.CMFPlone.CatalogTool import CatalogTool


def searchResults(self, REQUEST=None, **kw):
    has_search_text = kw.get("SearchableText", None)
    has_path = kw.get("path", None)
    # Internal means not a search by a user within search form
    isInternal = kw.get("object_provides", None)
    if has_search_text and isinstance(has_search_text, type({})):
        has_search_text = has_search_text.get("query", None)
        isInternal = True
    # user query, needs to be personalized
    if has_search_text and not isInternal:
        if has_path:
            path = kw["path"]
            # Make sure we only search in the content area
            kw["path"] = "%s/content" % path
        if has_search_text[-1] != "*":
            kw["SearchableText"] = has_search_text + "*"
        scns = getScenariosForCurrentUser()
        rqurl = ""
        if hasattr(self.REQUEST, "URL"):
            rqurl = self.REQUEST["URL"]
        isArchive = rqurl.find("/archive/") > -1
        if not isArchive:
            if scns:
                kw["scenarios"] = scns
            else:  # If we don't have a filter
                kw["scenarios"] = ["dontfindanything"]
    return self.original_searchResults(REQUEST, **kw)


if not hasattr(CatalogTool, "original_searchResults"):
    CatalogTool.original_searchResults = CatalogTool.searchResults
    CatalogTool.searchResults = searchResults
    CatalogTool.__call__ = searchResults
