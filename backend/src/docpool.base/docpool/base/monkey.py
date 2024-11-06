from Acquisition import aq_get
from docpool.base.utils import possibleDocTypes
from docpool.base.utils import possibleDocumentPools
from Products.PlonePAS.tools.groupdata import GroupDataTool
from Products.ZCatalog.CatalogBrains import AbstractCatalogBrain
from zope.globalrequest import getRequest

import ssl


def getURL(self, relative=0, original=False):
    """
    Patched so we can provide special URLs for category documents in listings
    such as livesearch. The category objects are viewed within a collections (see @@dview)
    Also we make sure that sections don't get an URL, so they are not linked to in the navigation.
    """
    request = aq_get(self, "REQUEST", None)
    if request is None:
        request = getRequest()
    if (
        # original set we ignore this special code
        (not original)
        # only valid for DPDocuments
        and self.portal_type == "DPDocument"
        # resolveid does not exist in url
        and not request["URL"].find("resolveuid") > -1
        and not request["URL"].find("Transfers") > -1
        or "overview" in str(request.get("myfolder_url", "/"))
    ):
        if self.cat_path:
            # This is it: we use the path of the category
            return f"{self.cat_path}/@@dview?d={self.UID}&disable_border=1"
        else:
            pass

    # This is the normal implementation
    return request.physicalPathToURL(self.getPath(), relative)


if not hasattr(AbstractCatalogBrain, "original_getURL"):
    AbstractCatalogBrain.original_getURL = AbstractCatalogBrain.getURL
    AbstractCatalogBrain.getURL = getURL


ssl._create_default_https_context = ssl._create_unverified_context


# XXX PropertyManagers expect methods called to provide options for select variables to
# be available as an object attribute. Should be modernised some day.
GroupDataTool.possibleDocTypes = possibleDocTypes
GroupDataTool.possibleDocumentPools = possibleDocumentPools
