from docpool.base.utils import _copyPaste
from Products.CMFCore.utils import getToolByName

HAS_ELAN = True
try:
    from docpool.elan.config import ELAN_APP
except BaseException:
    HAS_ELAN = False


def ensureDocTypeInTarget(original, copy):
    my_dt = original.docType
    config = copy.myDocumentPool().config.dtypes
    if config.hasObject(my_dt):
        return
    dtObj = original.docTypeObj()
    id = _copyPaste(dtObj, config)
    new_dt = config._getOb(id)
    if HAS_ELAN:
        new_dt.doc_extension(ELAN_APP).setCCategory(
            "recent"
        )  # Set intermediate category
    wftool = getToolByName(original, "portal_workflow")
    wftool.doActionFor(new_dt, "retract")
    new_dt.reindexObject()
    new_dt.reindexObjectSecurity()
    config.reindexObject()
